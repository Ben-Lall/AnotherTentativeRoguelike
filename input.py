from bearlibterminal import terminal as blt


def handle_input(player, world):
    """Handle this player's current input queue."""
    while blt.has_input():
        handle_key(player, world)


def handle_key(player, world):
    """Handle this player's next input key."""
    key = blt.read()

    if key == blt.TK_CLOSE:
        exit()

    if key == blt.TK_RESIZED:
        w = blt.state(blt.TK_WIDTH)
        h = blt.state(blt.TK_HEIGHT)
        player.camera.resize(w, h)

    # NESW Movement
    if key == blt.TK_KP_8:
        player.move(0, -1, world)
    elif key == blt.TK_KP_6:
        player.move(1, 0, world)
    elif key == blt.TK_KP_2:
        player.move(0, 1, world)
    elif key == blt.TK_KP_4:
        player.move(-1, 0, world)

    # Diagonal Movement
    elif key == blt.TK_KP_7:
        player.move(-1, -1, world)
    elif key == blt.TK_KP_9:
        player.move(1, -1, world)
    elif key == blt.TK_KP_3:
        player.move(1, 1, world)
    elif key == blt.TK_KP_1:
        player.move(-1, 1, world)
