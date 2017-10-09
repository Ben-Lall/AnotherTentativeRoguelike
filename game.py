from bearlibterminal import terminal as blt
from player import Player
from world import World
import input
import time


class Game:
    """"The main game loop.  Manages game logic and rendering."""

    # Game loop speed settings
    TICKS_PER_SECOND = 25
    SKIP_TICKS = 1000 / TICKS_PER_SECOND
    MAX_FRAMESKIP = 5

    def __init__(self):
        # open terminal
        blt.open()
        blt.refresh()

        # set up tick counting
        self.next_game_tick = self.elapsed_time()

        # Place the player
        World.add_player(Player(World))

    def iterate(self):
        """Perform one iteration of the game loop."""
        concurrent_update_loops = 0
        thing = self.elapsed_time()
        while self.elapsed_time() > self.next_game_tick and concurrent_update_loops < self.MAX_FRAMESKIP:
            self.update()
            self.next_game_tick += self.SKIP_TICKS
            concurrent_update_loops += 1

        interpolation = min((self.elapsed_time() + self.SKIP_TICKS - self.next_game_tick) / float(self.SKIP_TICKS), 1.0)
        self.render(interpolation)

    def update(self):
        """Update all game logic"""

        input.handle_input(World.active_player)


    def render(self, interpolation):
        """Render all on-screen objects."""
        blt.clear()

        World.active_player.render_screen(World)

        blt.bkcolor(blt.color_from_argb(255, 0, 0, 0))

        blt.refresh()

    def elapsed_time(self):
        """Return the amount of milliseconds that have elapsed since the system has started.  Will likely break upon around 24.855 hours of concurrent execution, but whatever."""
        return time.process_time() * 1000
