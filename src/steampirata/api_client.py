import http.client
import json
import time
import urllib.error
import urllib.request

from steampirata import config
from steampirata.errors import (
    ApiAuthError,
    ApiConfigError,
    ApiConnectionError,
    ApiDataError,
    ApiError,
    ApiNotFoundError,
    ApiServerError,
    ApiTimeoutError,
)
from steampirata.game import Game


class GamesApiClient:
    """Downloads the list of games from the API.

    Every problem is converted into a subclass of ApiError whose message can
    be shown directly to the user. Server failures and lost connections are
    retried a few times before giving up.
    """

    def __init__(
        self,
        url: str | None = None,
        api_key: str | None = None,
        timeout: float | None = None,
        retries: int | None = None,
        retry_delay: float | None = None,
    ):
        """Create the client. Values that are not given are read from config.py.

        Args:
            url: Address of the games endpoint.
            api_key: Key sent in the X-API-Key header.
            timeout: Seconds to wait for each answer.
            retries: Extra attempts after a server or connection failure.
            retry_delay: Seconds to wait between attempts.
        """
        self.url = config.API_URL if url is None else url
        self.api_key = config.API_KEY if api_key is None else api_key
        self.timeout = config.API_TIMEOUT if timeout is None else timeout
        self.retries = config.API_RETRIES if retries is None else retries
        self.retry_delay = config.API_RETRY_DELAY if retry_delay is None else retry_delay

    def fetch_games(self) -> list[Game]:
        """Download the games, retrying when the failure may be temporary.

        Returns:
            The games sent by the API.

        Raises:
            ApiError: A subclass that explains what went wrong.
        """
        attempt = 0
        while True:
            try:
                return self._parse_games(self._download())
            except (ApiServerError, ApiConnectionError):
                attempt += 1
                if attempt > self.retries:
                    raise
                time.sleep(self.retry_delay)

    def _download(self) -> bytes:
        """Send the request and return the raw answer.

        Raises:
            ApiConfigError: There is no API key.
            ApiAuthError: The key was rejected (401 or 403).
            ApiNotFoundError: The address does not exist (404).
            ApiServerError: The server failed (5xx).
            ApiTimeoutError: The server took too long.
            ApiConnectionError: The server could not be reached.
        """
        if not self.api_key:
            raise ApiConfigError("Falta la API key. Colócala en config.py (API_KEY).")

        request = urllib.request.Request(
            self.url,
            headers={"X-API-Key": self.api_key, "Accept": "application/json"},
        )
        # The request to the API is made here with urllib (standard library, so no
        # extra dependency is needed). Every network failure is caught below
        # and converted into an ApiError that the interface can explain.
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            raise self._error_from_status(error.code) from error
        except urllib.error.URLError as error:
            if isinstance(error.reason, TimeoutError):
                raise self._timeout_error() from error
            raise ApiConnectionError(
                "No se pudo conectar con el servidor. Revisa tu conexión a internet."
            ) from error
        except TimeoutError as error:
            raise self._timeout_error() from error
        except (OSError, http.client.HTTPException) as error:
            raise ApiConnectionError("Se perdió la conexión con el servidor.") from error

    def _timeout_error(self) -> ApiTimeoutError:
        """Build the error used when the server does not answer in time."""
        return ApiTimeoutError(
            f"El servidor tardó más de {self.timeout:g} segundos en responder. "
            "Puede estar despertando; intenta de nuevo."
        )

    @staticmethod
    def _error_from_status(status: int) -> ApiError:
        """Convert an HTTP error code into the matching ApiError.

        Args:
            status: HTTP status code sent by the server.
        """
        if status == 401:
            return ApiAuthError("La API pide una API key y no se envió ninguna (401).")
        if status == 403:
            return ApiAuthError("La API key no es válida para este usuario (403).")
        if status == 404:
            return ApiNotFoundError(
                "No se encontró la dirección en la API (404). Revisa API_URL en config.py."
            )
        return ApiServerError(f"El servidor de la API tuvo un problema (código {status}).")

    @staticmethod
    def _parse_games(raw: bytes) -> list[Game]:
        """Convert the JSON sent by the API into Game objects.

        Args:
            raw: Body of the answer.

        Raises:
            ApiDataError: The JSON is invalid, incomplete or has no games.
        """
        try:
            data = json.loads(raw.decode("utf-8"))
            games = [
                Game(
                    title=item["title"],
                    price=float(item["price"]),
                    genre=item["genre"],
                    description=item["description"],
                )
                for item in data["items"]
            ]
        except (ValueError, KeyError, TypeError) as error:
            raise ApiDataError(
                "La respuesta de la API no tiene el formato esperado."
            ) from error
        if not games:
            raise ApiDataError("La API no devolvió ningún juego.")
        return games
