from bearlibterminal import terminal as blt


def handle_input(player):
    """Handle this player's current input queue."""
    while blt.has_input():
        handle_key(player)


def handle_key(player):
    """Handle this player's next input key."""
    key = blt.read()

    # NESW Movement
    if key == blt.TK_KP_8:
        player.move(0, -1)
    elif key == blt.TK_KP_6:
        player.move(1, 0)
    elif key == blt.TK_KP_2:
        player.move(0, 1)
    elif key == blt.TK_KP_4:
        player.move(-1, 0)

    # Diagonal Movement
    elif key == blt.TK_KP_7:
        player.move(-1, -1)
    elif key == blt.TK_KP_9:
        player.move(1, -1)
    elif key == blt.TK_KP_3:
        player.move(1, 1)
    elif key == blt.TK_KP_1:
        player.move(-1, 1)
