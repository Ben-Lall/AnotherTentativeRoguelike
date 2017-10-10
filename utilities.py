import random


def get_random_tile():
    """Return the point of a random unobstructed tile."""
    return(random.randint(0, 20), random.randint(0, 20))

def clamp(val, minimum, maximum):
    """Clamp the given value to the bounds of [min, max]."""
    return max(minimum, min(val, maximum))
