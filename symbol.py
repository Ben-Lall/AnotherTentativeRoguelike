class Symbol:
    """A more complex character that has color and displacement."""
    def __init__(self, char, color, dx=0, dy=0):
        self.color = color
        self.char = char
        self.dx = dx
        self.dy = dy
