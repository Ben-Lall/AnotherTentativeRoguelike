from bearlibterminal import terminal as blt


def handle_input(player, world):
    """Handle this player's current input queue."""
    turn_ended = False
    while not turn_ended:
        key = blt.read()
        turn_ended = handle_key(key, player, world)


def handle_key(key, player, world):
    """Handle this player's next input key.  Return whether or not the input represents an action that ends the turn."""

    if key == blt.TK_CLOSE:
        exit()

    if key == blt.TK_RESIZED:
        w = blt.state(blt.TK_WIDTH)
        h = blt.state(blt.TK_HEIGHT)
        player.camera.resize(w, h)
        return False

    # NESW Movement
    if key == blt.TK_KP_8:
        return player.move(0, -1, world)
    elif key == blt.TK_KP_6:
        return player.move(1, 0, world)
    elif key == blt.TK_KP_2:
        return player.move(0, 1, world)
    elif key == blt.TK_KP_4:
        return player.move(-1, 0, world)

    # Diagonal Movement
    elif key == blt.TK_KP_7:
        return player.move(-1, -1, world)
    elif key == blt.TK_KP_9:
        return player.move(1, -1, world)
    elif key == blt.TK_KP_3:
        return player.move(1, 1, world)
    elif key == blt.TK_KP_1:
        return player.move(-1, 1, world)
