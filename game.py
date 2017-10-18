from bearlibterminal import terminal as blt
from player import Player
from world import World
import colors
import input


class Game:
    """"The main game loop.  Manages game logic and rendering."""

    # Game loop speed settings
    TICKS_PER_SECOND = 25
    SKIP_TICKS = 1000 / TICKS_PER_SECOND
    MAX_FRAMESKIP = 5

    def __init__(self):
        # Open terminal
        blt.open()
        blt.refresh()

        # Set up the terminal
        blt.set("window: title='Roguelike', cellsize=12x12, resizeable=true, size=80x45, minimum-size=27x5; ini.settings.tile-size=16;")

        # Create world
        self.world = World()
        start_pos = self.world.generate_floor()
        self.world.add_player(Player(start_pos, self.world))
        self.render()

    def iterate(self):
        """Perform one iteration of the game loop."""
        self.update()
        self.render()

    def update(self):
        """Update all game logic"""
        for c in (c for c in self.world.current_floor_creatures if c != self.world.active_player):
            c.take_turn(self.world)

        input.handle_input(self.world.active_player, self.world)
        self.world.active_player.update_memory_map(self.world)

    def render(self):
        """Render all on-screen objects."""
        blt.clear()

        self.world.active_player.render_screen(self.world)

        blt.bkcolor(colors.CLEAR)

        blt.refresh()
