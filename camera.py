class Camera:
    """A camera that is used for rendering a specific region."""

    def __init__(self, x, y):
        self.x = x
        self. y = y

    def render(self, world, renderer):
        """Render all the things in the world visible by this camera."""

        # Draw all visible tiles (temporary implementation)
        for i in range(0, world.FLOOR_HEIGHT):
            for j in range(0, world.FLOOR_WIDTH):
                tile = world.current_floor[i][j]
                tile.render(j, i, renderer)

        # Draw all visible gameplay objects (temporary implementation)
        for e in world.current_floor_elements:
            e.render(renderer)
