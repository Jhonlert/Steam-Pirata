import flet as ft

from steampirata.game import Game


class GameCover:
    """Builds the visual pieces that depend on the genre of a game."""

    # Main color and possible emojis for each genre (keys in lowercase).
    GENRE_STYLES = {
        "acción": ("#e74c3c", ["⚔️", "💥", "🎯"]),
        "aventura": ("#3498db", ["🧭", "🗺️", "⛵"]),
        "supervivencia": ("#27ae60", ["🏝️", "🔥", "🌴"]),
        "puzzle": ("#9b59b6", ["🧩", "🔑", "🔮"]),
        "estrategia": ("#f39c12", ["♟️", "💰", "🦜"]),
    }
    DEFAULT_STYLE = ("#16a085", ["🎮", "🕹️", "👾"])

    # Dark colors mixed with the genre color, so games of the same genre differ.
    DARK_TONES = ["#1b1f4b", "#2d1b4e", "#0f3d4a", "#4a1b2e", "#1f3b2d", "#3b2a14"]

    @staticmethod
    def get_style(genre: str) -> tuple[str, list[str]]:
        """Return the (color, emojis) pair of a genre.

        Args:
            genre: Genre name, in any case.

        Returns:
            A default style if the genre is not in GENRE_STYLES.
        """
        return GameCover.GENRE_STYLES.get(genre.lower(), GameCover.DEFAULT_STYLE)

    @staticmethod
    def _seed(title: str) -> int:
        """Return a number that depends only on the title (always the same)."""
        return sum(ord(letter) for letter in title)

    @staticmethod
    def build_genre_chip(genre: str) -> ft.Container:
        """Return a small colored label with the genre name."""
        color, _ = GameCover.get_style(genre)
        return ft.Container(
            content=ft.Text(genre, size=11, weight=ft.FontWeight.BOLD, color="#ffffff"),
            bgcolor=color,
            padding=ft.Padding.symmetric(horizontal=10, vertical=3),
            border_radius=10,
        )

    @staticmethod
    def build(game: Game, width: int, height: int) -> ft.Container:
        """Return the cover of a game: a color gradient with an emoji.

        It is drawn by the program itself, so it works without internet.
        The same title always gets the same cover.

        Args:
            game: Game that needs a cover.
            width: Width of the cover in pixels.
            height: Height of the cover in pixels.
        """
        color, emojis = GameCover.get_style(game.genre)
        seed = GameCover._seed(game.title)
        emoji = emojis[seed % len(emojis)]
        dark = GameCover.DARK_TONES[seed % len(GameCover.DARK_TONES)]
        return ft.Container(
            width=width,
            height=height,
            border_radius=8,
            alignment=ft.Alignment.CENTER,
            gradient=ft.LinearGradient(
                colors=[color, dark],
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
            ),
            content=ft.Text(emoji, size=height // 2),
        )
