# SteamPirata ☠

Tienda de videojuegos de mentira hecha con Python con flet. Los juegos se descargan de una API
y, si la API falla, la tienda sigue funcionando con un catálogo local.


## Qué hace

- Tres pantallas: tienda, detalle del juego y carrito.
- Buscador por título o género, botón 🎲 (juego al azar) y portadas de color según el género.
- Carrito: agregar, quitar, total y compra **simulada** (no se guarda nada).
- Descarga los juegos de la API del profesor, con pantalla de carga, aviso de errores y botón "Reintentar".

## Cómo ponerlo a andar

Requisitos: [uv](https://docs.astral.sh/uv/) e internet (solo para la API).

```
uv sync
uv run steampirata
```

## Dependencias

- **flet**: única librería externa (la instala `uv sync`).
- Para hablar con la API se usa **`urllib`**, que ya viene con Python. No se usa `requests` a propósito:
  así no hay una dependencia más que mantener.

## Configuración de la API

Todo está en `src/steampirata/config.py`:

| Ajuste | Para qué sirve |
|---|---|
| `API_URL` | Endpoint `GET /api/v1/jhonlert/games` |
| `API_KEY` | Clave que se envía en la cabecera `X-API-Key`|
| `API_TIMEOUT` | Segundos de espera por la respuesta |
| `API_RETRIES` / `API_RETRY_DELAY` | Reintentos automáticos y pausa entre ellos |

> La API key es personal.
> El servidor gratuito (Render) puede tardar hasta un minuto en despertar la primera vez.

## Arquitectura

```
Pantallas (Flet)          Lógica                    Acceso a datos
StoreScreen  ┐
DetailScreen ├─ SteamPirataApp ─┬─ Store ◄── ApiStore ──► GamesApiClient ──► API
CartScreen   ┘                  └─ Cart                         │
                                                          errors.py (ApiError y subclases)
```

- `Game`: la ficha de cada juego (con un método estático `format_price`).
- `Store`: catálogo local y buscador. `ApiStore` **hereda** de `Store` y solo cambia de dónde salen los juegos.
- `GamesApiClient`: hace la petición HTTP, convierte la respuesta en `Game` y traduce cada fallo a un error propio.
- `Cart`: el carrito y su total.
- `GameCover`: dibuja la portada y el color de cada género (sin internet).
- `SteamPirataApp`: tiene la tienda y el carrito y decide qué pantalla se ve.

## Dónde se manejan los errores

| Archivo | Función | Qué controla |
|---|---|---|
| `api_client.py` | `_download()` | **El request a la API.** Captura `HTTPError` (401, 403, 404, 5xx), `URLError` (sin internet), `TimeoutError` y cortes de conexión |
| `api_client.py` | `_parse_games()` | JSON roto, campos que faltan o precios inválidos |
| `api_client.py` | `fetch_games()` | Reintenta si el fallo puede ser temporal (servidor caído o conexión perdida) |
| `api_store.py` | `load()` | Captura cualquier `ApiError`, usa el catálogo local y guarda el motivo para mostrarlo |

Cada fallo se convierte en una subclase de `ApiError` (`errors.py`) con un mensaje claro para el usuario:

| Situación | Error | Qué ve el usuario |
|---|---|---|
| No hay API key | `ApiConfigError` | Aviso rojo y catálogo local |
| Clave rechazada (401, 403) | `ApiAuthError` | Aviso rojo y catálogo local |
| Dirección incorrecta (404) | `ApiNotFoundError` | Aviso rojo y catálogo local |
| Servidor caído (5xx) | `ApiServerError` | Reintenta solo; si sigue fallando, aviso rojo |
| Sin internet o conexión perdida | `ApiConnectionError` | Reintenta solo; si sigue fallando, aviso rojo |
| El servidor tarda demasiado | `ApiTimeoutError` | Aviso rojo con botón "Reintentar" |
| JSON roto, incompleto o vacío | `ApiDataError` | Aviso rojo y catálogo local |

Mientras se descargan los datos se muestra una pantalla de carga. El indicador de arriba muestra si se usa la
API (● verde) o el catálogo local (○ gris).

## Decisiones de diseño

- **Cliente y tienda separados:** `GamesApiClient` solo sabe de HTTP y `ApiStore` solo sabe de catálogo.
  Así se puede cambiar uno sin tocar el otro.
- **Catálogo local de respaldo:** si la API falla, la tienda no queda vacía.
- **Pantallas como clases propias:** `SteamPirataApp` cambia el contenido de la página. No se usó el sistema
  de rutas de Flet para mantenerlo simple.
- **Portadas dibujadas por el programa:** no dependen de internet ni de archivos de imagen.

## Limitaciones conocidas

- Solo se usa un endpoint (`GET /games`).
- Los juegos se descargan al abrir la aplicación o al pulsar "Reintentar", no se actualizan solos.
- El carrito y la compra no se guardan.
- No hay pruebas automáticas.

## Cómo extender

- **Nuevo género con color y emoji:** agregarlo en `GENRE_STYLES` de `game_cover.py`.
- **Cambiar de API o de clave:** editar `config.py`.
- **Nueva pantalla:** crear una clase como `CartScreen` y un método `show_...` en `app.py`.

## Estructura

```
src/steampirata/
├── __init__.py       # arranque
├── app.py            # SteamPirataApp: pantallas, carga y reintento
├── config.py         # ajustes de la API
├── errors.py         # errores propios (ApiError y subclases)
├── api_client.py     # GamesApiClient: HTTP y manejo de errores
├── api_store.py      # ApiStore: catálogo desde la API
├── store.py          # Store: catálogo local y buscador
├── game.py           # Game
├── game_cover.py     # GameCover
├── cart.py           # Cart
├── store_screen.py   # pantalla de la tienda
├── detail_screen.py  # pantalla de detalle
└── cart_screen.py    # pantalla del carrito
```

Todos los módulos, clases y métodos tienen docstrings. El código está en inglés y los textos de la
interfaz en español.

## Historial

- **v1:** catálogo local, buscador y carrito en una sola pantalla.
- **v2:** pantallas separadas y método estático.
- **v3:** pantalla de detalle y portadas.
- **v4:** conexión con la API del profesor.
- **v5:** manejo de errores de red (errores propios, reintentos y avisos en pantalla).
