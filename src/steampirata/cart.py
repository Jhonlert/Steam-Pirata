from steampirata.game import Game


class Cart:
    """Stores the games the user wants to buy."""

    def __init__(self):
        """Create an empty cart."""
        self.items: list[Game] = []

    def add(self, game: Game) -> bool:
        """Add a game to the cart.

        Args:
            game: Game to add.

        Returns:
            True if it was added, False if it was already in the cart.
        """
        if game in self.items:
            return False
        self.items.append(game)
        return True

    def remove(self, game: Game) -> None:
        """Remove a game from the cart if it is there."""
        if game in self.items:
            self.items.remove(game)

    def clear(self) -> None:
        """Remove every game from the cart."""
        self.items.clear()

    def get_items(self) -> list[Game]:
        """Return the games currently in the cart."""
        return self.items

    def get_total(self) -> float:
        """Return the sum of the prices of all games in the cart."""
        return sum(game.price for game in self.items)
