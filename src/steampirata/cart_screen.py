from typing import TYPE_CHECKING

import flet as ft

from steampirata.game import Game

if TYPE_CHECKING:
    from steampirata.app import SteamPirataApp


class CartScreen:
    """Screen that shows the shopping cart."""

    def __init__(self, app: "SteamPirataApp"):
        """Create the widgets of the screen.

        Args:
            app: Main application, used to reach the cart and navigation.
        """
        self.app = app
        self.cart_list = ft.ListView(expand=True, spacing=5)
        self.total_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
        self.status_text = ft.Text("", color="#4cd964")

    def build(self) -> ft.Column:
        """Return the full layout of the screen."""
        header = ft.Row(
            [
                ft.Text(
                    "Carrito",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#f5b942",
                    expand=True,
                ),
                ft.Button("← Volver a la tienda", on_click=lambda e: self.app.show_store()),
            ]
        )
        self._fill_cart()
        return ft.Column(
            [
                header,
                self.cart_list,
                self.total_text,
                ft.Button("Comprar", on_click=self.on_buy),
                self.status_text,
            ],
            expand=True,
        )

    def _build_row(self, game: Game) -> ft.Row:
        """Return one row of the cart with a remove button."""
        return ft.Row(
            [
                ft.Text(game.title, expand=True),
                ft.Text(game.get_price_label()),
                ft.Button("Quitar", on_click=lambda e, g=game: self.on_remove(g)),
            ]
        )

    def _fill_cart(self) -> None:
        """Put one row per game and update the total (does not refresh the page)."""
        rows = [self._build_row(game) for game in self.app.cart.get_items()]
        self.cart_list.controls = rows or [ft.Text("El carrito está vacío")]
        total = Game.format_price(self.app.cart.get_total())
        self.total_text.value = f"Total: {total}"

    def on_remove(self, game: Game) -> None:
        """Remove the game from the cart."""
        self.app.cart.remove(game)
        self._fill_cart()
        self.app.page.update()

    def on_buy(self, e) -> None:
        """Simulate the purchase and empty the cart."""
        if not self.app.cart.get_items():
            self.status_text.value = "Agrega algún juego primero."
        else:
            total = Game.format_price(self.app.cart.get_total())
            self.app.cart.clear()
            self.status_text.value = f"¡Compra realizada! Pagaste {total} 🏴‍☠️"
        self._fill_cart()
        self.app.page.update()
