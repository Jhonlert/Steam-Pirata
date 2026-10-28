import random

from steampirata.game import Game


class Store:
    """Holds the game catalog and handles searching."""

    def __init__(self):
        """Create the store and load its games."""
        self.source_label = "Local"
        self.games = self._load_games()

    def _load_games(self) -> list[Game]:
        """Load the catalog. Subclasses can override this to change the source."""
        return self._load_local_games()

    def _load_local_games(self) -> list[Game]:
        """Return the hand-written list of games."""
        return [
            Game("Calavera Rebelde", 19.99, "Aventura", "Navega los siete mares en busca del tesoro perdido."),
            Game("Ron y Pólvora", 9.99, "Acción", "Defiende tu barco de oleadas de piratas enemigos."),
            Game("Isla Perdida", 0, "Supervivencia", "Sobrevive en una isla desierta llena de secretos."),
            Game("Kraken Rush", 24.99, "Acción", "Escapa de un monstruo marino gigante a toda velocidad."),
            Game("Mapa Maldito", 14.50, "Puzzle", "Resuelve acertijos para descifrar un mapa antiguo."),
            Game("Capitán Tacaño", 4.99, "Estrategia", "Administra tu flota sin quedarte sin monedas."),
            Game("Tormenta Negra", 29.99, "Aventura", "Un viaje épico a través de la peor tormenta del Caribe."),
            Game("Loro Parlanchín", 0, "Puzzle", "Ayuda a un loro a descubrir el código del cofre."),
        ]

    def get_all_games(self) -> list[Game]:
        """Return every game in the catalog."""
        return self.games

    def get_random_game(self) -> Game:
        """Return a random game from the catalog."""
        return random.choice(self.games)

    def search(self, query: str) -> list[Game]:
        """Return the games whose title or genre contains the query.

        Args:
            query: Text typed by the user (case-insensitive).

        Returns:
            The matching games, or all games if the query is empty.
        """
        query = query.strip().lower()
        if query == "":
            return self.games
        return [
            game for game in self.games
            if query in game.title.lower() or query in game.genre.lower()
        ]
