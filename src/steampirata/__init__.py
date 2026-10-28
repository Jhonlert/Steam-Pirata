import flet as ft

from steampirata.app import SteamPirataApp


def build(page: ft.Page) -> None:
    """Create the application inside the page Flet gives us."""
    SteamPirataApp(page)


def main() -> None:
    """Start the SteamPirata application."""
    ft.run(build)
