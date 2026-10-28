class Game:
    """Represents a video game in the store catalog."""

    def __init__(self, title: str, price: float, genre: str, description: str):
        """Create a game.

        Args:
            title: Name of the game.
            price: Price in dollars (0 means free).
            genre: Genre of the game (e.g. "Aventura").
            description: Short description shown in the interface.
        """
        self.title = title
        self.price = price
        self.genre = genre
        self.description = description

    @staticmethod
    def format_price(amount: float) -> str:
        """Format a number as dollars.

        It is a static method because it does not need the data of any
        specific game, so it can also be used for the cart total.

        Args:
            amount: Quantity of money to format.

        Returns:
            Text such as "$14.99".
        """
        return f"${amount:.2f}"

    def get_price_label(self) -> str:
        """Return the price of this game as text for the interface."""
        if self.price == 0:
            return "Gratis"
        return Game.format_price(self.price)
