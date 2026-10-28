from typing import TYPE_CHECKING

import flet as ft

from steampirata.game import Game
from steampirata.game_cover import GameCover

if TYPE_CHECKING:
    from steampirata.app import SteamPirataApp


class DetailScreen:
    """Screen that shows one game in detail."""

    def __init__(self, app: "SteamPirataApp", game: Game):
        """Create the screen.

        Args:
            app: Main application, used to reach the cart and navigation.
            game: Game to show.
        """
        self.app = app
        self.game = game
        self.status_text = ft.Text("", color="#4cd964")

    def build(self) -> ft.Column:
        """Return the full layout of the screen."""
        header = ft.Row(
            [
                ft.Text(
                    "Detalle del juego",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#f5b942",
                    expand=True,
                ),
                ft.Button("← Volver a la tienda", on_click=lambda e: self.app.show_store()),
                ft.Button("Ver carrito", on_click=lambda e: self.app.show_cart()),
            ]
        )
        info = ft.Column(
            [
                ft.Text(self.game.title, size=30, weight=ft.FontWeight.BOLD),
                GameCover.build_genre_chip(self.game.genre),
                ft.Text(self.game.description, size=16),
                ft.Text(self.game.get_price_label(), size=26, color="#4cd964"),
                ft.Button("Agregar al carrito", on_click=self.on_add),
                self.status_text,
            ],
            spacing=12,
            expand=True,
        )
        body = ft.Row(
            [GameCover.build(self.game, 380, 240), info],
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=24,
        )
        return ft.Column([header, body], spacing=20, expand=True)

    def on_add(self, e) -> None:
        """Add this game to the cart and tell the user."""
        if self.app.cart.add(self.game):
            self.status_text.value = "¡Agregado al carrito!"
        else:
            self.status_text.value = "Este juego ya está en el carrito."
        self.app.page.update()
