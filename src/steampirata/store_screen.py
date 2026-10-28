from typing import TYPE_CHECKING

import flet as ft

from steampirata.game import Game
from steampirata.game_cover import GameCover

if TYPE_CHECKING:
    from steampirata.app import SteamPirataApp


class StoreScreen:
    """Screen that shows the catalog of games."""

    def __init__(self, app: "SteamPirataApp"):
        """Create the widgets of the screen.

        Args:
            app: Main application, used to reach the store, the cart and navigation.
        """
        self.app = app
        self.search_field = ft.TextField(
            label="Buscar por título o género",
            on_change=self.on_search,
            expand=True,
        )
        self.catalog_list = ft.ListView(expand=True, spacing=10)
        self.cart_count_text = ft.Text("", color="#9aa0c8")
        self.source_text = ft.Text(size=12)

    def build(self) -> ft.Column:
        """Return the full layout of the screen."""
        header = ft.Row(
            [
                ft.Text(
                    "☠ SteamPirata",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#f5b942",
                    expand=True,
                ),
                self.source_text,
                self.cart_count_text,
                ft.Button("Ver carrito", on_click=lambda e: self.app.show_cart()),
            ]
        )
        surprise_button = ft.Button("🎲", tooltip="Sorpréndeme", on_click=self.on_surprise)
        show_all_button = ft.Button("Ver todos", on_click=self.on_show_all)
        search_row = ft.Row([self.search_field, surprise_button, show_all_button])

        self._update_source_text()
        self._update_cart_count()
        self._fill_catalog(self.app.store.get_all_games())
        return ft.Column([header, search_row, self.catalog_list], expand=True)

    def _build_game_card(self, game: Game) -> ft.Container:
        """Return the visual card of one game."""
        info = ft.Column(
            [
                ft.Text(game.title, size=18, weight=ft.FontWeight.BOLD),
                GameCover.build_genre_chip(game.genre),
                ft.Text(game.description, size=12),
            ],
            expand=True,
        )
        actions = ft.Column(
            [
                ft.Text(game.get_price_label(), size=16, color="#4cd964"),
                ft.Button("Detalle", on_click=lambda e, g=game: self.app.show_detail(g)),
                ft.Button("Agregar", on_click=lambda e, g=game: self.on_add(g)),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
        )
        return ft.Container(
            content=ft.Row([GameCover.build(game, 150, 96), info, actions]),
            bgcolor="#1a1f3d",
            padding=12,
            border_radius=10,
        )

    def _fill_catalog(self, games: list[Game]) -> None:
        """Put one card per game in the list (does not refresh the page)."""
        cards = [self._build_game_card(game) for game in games]
        self.catalog_list.controls = cards or [ft.Text("No se encontraron juegos")]

    def _update_source_text(self) -> None:
        """Show whether the games come from the API or from the local list."""
        if self.app.store.source_label == "API":
            self.source_text.value = "● API conectada"
            self.source_text.color = "#4cd964"
        else:
            self.source_text.value = "○ Catálogo local"
            self.source_text.color = "#9aa0c8"

    def _update_cart_count(self) -> None:
        """Show how many games are in the cart (does not refresh the page)."""
        self.cart_count_text.value = f"En el carrito: {len(self.app.cart.get_items())}"

    def on_search(self, e) -> None:
        """Filter the catalog every time the user types."""
        self._fill_catalog(self.app.store.search(self.search_field.value))
        self.app.page.update()

    def on_show_all(self, e) -> None:
        """Clear the search box and show the whole catalog again."""
        self.search_field.value = ""
        self._fill_catalog(self.app.store.get_all_games())
        self.app.page.update()

    def on_surprise(self, e) -> None:
        """Show one random game in the catalog."""
        self._fill_catalog([self.app.store.get_random_game()])
        self.app.page.update()

    def on_add(self, game: Game) -> None:
        """Add the game to the cart."""
        self.app.cart.add(game)
        self._update_cart_count()
        self.app.page.update()
