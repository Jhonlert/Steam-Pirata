import flet as ft

from steampirata.api_store import ApiStore
from steampirata.cart import Cart
from steampirata.cart_screen import CartScreen
from steampirata.detail_screen import DetailScreen
from steampirata.game import Game
from steampirata.store_screen import StoreScreen


class SteamPirataApp:
    """Owns the store and the cart, and decides which screen is visible."""

    def __init__(self, page: ft.Page):
        """Create the application and show the store screen.

        Args:
            page: Page that Flet gives to the application.
        """
        self.page = page
        self.store = ApiStore()
        self.cart = Cart()
        self._setup_page()
        self.show_store()

    def _setup_page(self) -> None:
        """Configure window title, theme and colors."""
        self.page.title = "SteamPirata"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#0f1226"
        self.page.padding = 20

    def _show(self, content: ft.Control) -> None:
        """Replace whatever is on the page with a new screen."""
        self.page.controls.clear()
        self.page.add(content)
        self.page.update()

    def show_store(self) -> None:
        """Go to the store screen."""
        self._show(StoreScreen(self).build())

    def show_detail(self, game: Game) -> None:
        """Go to the detail screen of a game."""
        self._show(DetailScreen(self, game).build())

    def show_cart(self) -> None:
        """Go to the cart screen."""
        self._show(CartScreen(self).build())
