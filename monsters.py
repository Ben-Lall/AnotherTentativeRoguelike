from creature import Creature
from symbol import Symbol
import colors


def orc(x, y):
    return Creature(x, y, Symbol('o', colors.ORC))
