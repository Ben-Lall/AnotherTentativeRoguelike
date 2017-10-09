import random
from world import World


def get_random_tile():
    """Return the point of a random unobstructed tile."""
    return(random.randint(0, 20), random.randint(0, 20))


def is_unobstructed(x, y):
    """Check if the given coordinates of the current floor is unobstructed."""
    return 0 <= x < World.FLOOR_WIDTH and \
           0 <= y < World.FLOOR_HEIGHT and \
           not World.current_floor[y][x].blocked


def clamp(val, minimum, maximum):
    """Clamp the given value to the bounds of [min, max]."""
    return max(minimum, min(val, maximum))
