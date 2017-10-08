import random

def get_random_tile():
    """Return the point of a random unobstructed tile."""
    return(random.randint(0, 20), random.randint(0, 20))
