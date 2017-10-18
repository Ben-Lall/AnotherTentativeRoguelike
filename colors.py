from bearlibterminal import terminal as blt

# System colors
CLEAR = blt.color_from_argb(255, 0, 0, 0)

# Game colors
FLOOR = blt.color_from_argb(255, 40, 30, 20)
FLOOR_FADED = blt.color_from_argb(255, 30, 20, 10)
WALL = blt.color_from_argb(255, 20, 10, 0)
WALL_FADED = blt.color_from_argb(255, 14, 7, 0)

# World generation colors
WORLD_GEN_OPENING = blt.color_from_argb(255, 0, 120, 0)
WORLD_GEN_HIGHLIGHT = blt.color_from_argb(255, 153, 102, 51)
WORLD_GEN_CYCLE = blt.color_from_argb(255, 160, 230, 160)
