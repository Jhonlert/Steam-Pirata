import json
import urllib.request

from steampirata import config
from steampirata.game import Game
from steampirata.store import Store


class ApiStore(Store):
    """Store that reads its games from the API.

    It inherits everything from Store (search, random game...) and only
    changes where the games come from. If the API cannot be used, it falls
    back to the local catalog so the application never breaks.
    """

    def _load_games(self) -> list[Game]:
        """Load the games from the API, or from the local catalog if it fails."""
        if not config.API_KEY:
            print("[SteamPirata] No hay API key en config.py: se usa el catálogo local.")
            return self._load_local_games()
        try:
            games = self._fetch_games()
            self.source_label = "API"
            print(f"[SteamPirata] Conectado a la API: {len(games)} juegos cargados.")
            return games
        except Exception as error:  # Any failure must not close the app.
            print(f"[SteamPirata] No se pudo usar la API ({error}): se usa el catálogo local.")
            return self._load_local_games()

    def _fetch_games(self) -> list[Game]:
        """Download the games and convert them into Game objects.

        Returns:
            The games sent by the API.

        Raises:
            ValueError: If the API answers with an empty list.
        """
        request = urllib.request.Request(
            config.API_URL,
            headers={"X-API-Key": config.API_KEY, "Accept": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=config.API_TIMEOUT) as response:
            data = json.loads(response.read().decode("utf-8"))

        games = [
            Game(
                title=item["title"],
                price=float(item["price"]),
                genre=item["genre"],
                description=item["description"],
            )
            for item in data["items"]
        ]
        if not games:
            raise ValueError("la API no devolvió juegos")
        return games
