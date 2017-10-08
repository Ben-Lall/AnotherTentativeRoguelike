class GameplayObject():
    """A generic object in the game world, such as a creature or item."""

    def __init__(self, symbol, x, y):
        """Create a new GameplayObject at the given location."""
        self.symbol = symbol
        self.x = x
        self.y = y
        self.velocity = (0, 0)

    def render(self, renderer, layer):
        """Render this gameplay object."""
        if isinstance(self.symbol, list):
            renderer.render_composite(self.x, self.y, self.symbol, layer)
        else:
            renderer.render(self.x, self.y, self.symbol, layer)
