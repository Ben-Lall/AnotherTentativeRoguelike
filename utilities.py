import random
import math


def get_random_tile():
    """Return the point of a random unobstructed tile."""
    return random.randint(0, 20), random.randint(0, 20)


def clamp(val, minimum, maximum):
    """Clamp the given value to the bounds of [min, max]."""
    return max(minimum, min(val, maximum))


def euc_distance(start, destination):
    return math.sqrt(math.pow(start[0] - destination[0], 2) + math.pow(start[1] - destination[1], 2))


def is_in_bounds(floor, x, y):
    """Determine if the given coordinates are within the bounds of the floor."""
    return 0 <= x < len(floor[0]) and 0 <= y < len(floor)
