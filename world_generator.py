from enum import Enum
from symbol import Symbol
from renderer import Renderer
from camera import Camera
import world
from bearlibterminal import terminal as blt
import random as rand
import math
import time

ANIMATE_WORLD_GEN = False
ANIMATION_FRAME_LENGTH = 500  # Measured in milliseconds
ANIMATION_RENDERER = Renderer()
ANIMATION_CAMERA = None

START_WIDTH = 11
START_HEIGHT = 6

MAX_ROOMS = 59  # Assume the start room has already been placed.
MAX_ROOM_GENERATION_ATTEMPTS = 500


class _GenTile:
    """A tile containing extra information needed strictly for world generation."""
    def __init__(self, obstructed):
        self.obstructed = obstructed

    def render(self, x, y, renderer):
        """Render this tile at the given world coordinates."""
        if self.obstructed:
            bkcolor = blt.color_from_argb(255, 0, 0, 50)
        else:
            bkcolor = blt.color_from_argb(255, 0, 0, 30)
        renderer.render(x, y, Symbol(' ', blt.color_from_name("white")), 0, bkcolor)


class _RoomType(Enum):
    """Enumerator cataloguing the different shapes of rooms."""
    RECTANGLE = 0
    START = 60
    RANDOM = 100

    @staticmethod
    def generic_rooms():
        """Returns a list of generic, non-unique room types."""
        return [_RoomType.RECTANGLE]


class _Room:
    """A set of points, with some being potential openings.  A in a room point exists on an abstract canvas, and only serve
    to provide relative positioning to other points."""

    def __init__(self, room_type=_RoomType.RANDOM):
        self.body = set()  # A set of points that make up this room.
        self.openings = set()  # A set containing the openings of this room.  self.body ∩ self.openings = ∅

        if room_type == _RoomType.RANDOM:
            room_type = rand.choice(_RoomType.generic_rooms())

        if room_type == _RoomType.RECTANGLE:
            self.__add_rectangle(0, 0)
        elif room_type == _RoomType.START:
            self.__add_start()

    def __add_rectangle(self, x, y):
        """Overlap a rectangle starting at the given coordinates to this room."""
        width = rand.randint(6, 12)
        height = rand.randint(5, 10)
        for i in range(y, y + height):
            for j in range(x, x + width):
                self.body.add((j, i))
                if (j, i) in self.openings: self.openings.remove((j, i))

        # Add new openings

        # Top / bottom side
        exit_pos = (x + rand.randint(1, width - 2), y - 1)
        if exit_pos not in self.body: self.openings.add(exit_pos)
        exit_pos = (x + rand.randint(1, width - 2), y + height)
        if exit_pos not in self.body: self.openings.add(exit_pos)

        # Left / right side
        exit_pos = (x - 1, y + rand.randint(1, height - 2))
        if exit_pos not in self.body: self.openings.add(exit_pos)
        exit_pos = (x + width, y + rand.randint(1, height - 2))
        if exit_pos not in self.body: self.openings.add(exit_pos)

    def __add_start(self):
        width = START_WIDTH
        height = START_HEIGHT
        for i in range(0, height):
            for j in range(0, width):
                self.body.add((j, i))
        self.openings.add((int(math.ceil(width / 2)), -1))

    def add_to_blueprint(self, blueprint, world_openings):
        """Add this room to the given blueprint, if possible.  Returns the point of conjunction, if it is added."""

        # get a set of pairs of openings containing the pairs of world and self openings that would accomodate this room.
        # i.e.  return o ∈ (world_openings × self.openings) : the open tiles of blueprint and self.body contain no overlap if both elements of o were to be overlapped."""
        valid_opening_pairs = []
        for (wox, woy) in world_openings:
            for (rox, roy) in self.openings:
                # Test if this pair yields a placeable room that would not overlap or be adjacent to an existing room.
                placeable = True
                for (x, y) in self.body:
                    projected_tile = x - rox + wox, y - roy + woy
                    if not _valid_placement_pos(blueprint, projected_tile):
                        placeable = False
                        break

                if placeable: valid_opening_pairs.append(((wox, woy), (rox, roy)))

        # Draw a the room to a random pair, if any exist.
        if len(valid_opening_pairs) > 0:
            opening_pair = rand.choice(valid_opening_pairs)
            self._draw_to_blueprint_from_openings(blueprint, world_openings, opening_pair[0], opening_pair[1])
            return opening_pair[0]

    def _draw_to_blueprint_from_openings(self, blueprint, world_openings, world_opening, room_opening):
        """Assumes no overlap between blueprint and T(x, y)(self.body), where T is the translation function.  Updates openings to reflect room addition."""
        blueprint[world_opening[1]][world_opening[0]].obstructed = False
        world_openings.remove(world_opening)
        self.draw_to_blueprint(blueprint, world_openings, world_opening[0] - room_opening[0], world_opening[1] - room_opening[1])

    def draw_to_blueprint(self, blueprint, openings, x, y):
        """Assumes no overlap between blueprint and T(x, y)(self.body), where T is the translation function.  Updates openings to reflect room addition."""
        for (p1, p2) in self.body:
            blueprint[p2 + y][p1 + x].obstructed = False
            # for o in [(o1, o2) for (o1, o2) in openings if o1 == p1 and o2 == p2]:
            #     openings.remove(o)

        for (p1, p2) in self.openings:
            # Some openings may be obstructed since they lie outside of this.body
            if _is_in_bounds(blueprint, p1 + x, p2 + y) and blueprint[p2 + y][p1 + x].obstructed:
                openings.add((p1 + x, p2 + y))

    def render(self, renderer):
        for tile in self.body:
            renderer.render(10 + tile[0], 5 + tile[1], Symbol(' ', blt.color_from_name("white")), 0, blt.color_from_argb(255, 0, 0, 30))
        for opening in self.openings:
            renderer.render(10 + opening[0], 5 + opening[1], Symbol('V', blt.color_from_name("white")), 0, blt.color_from_argb(255, 0, 120, 0))


def generate_floor(floor):
    """Generate rooms and corridors for the given floor.  Expects a floor of completely blocked tiles, and the
    floor will be "carved" out of the existing floor."""
    blueprint = [[_GenTile(True) for x in range(len(floor[0]))] for y in range(len(floor))]
    world.blueprint = blueprint
    openings = set()  # Set of all available openings
    if ANIMATE_WORLD_GEN:
        global ANIMATION_CAMERA
        ANIMATION_CAMERA = Camera(0, 0, len(floor[0]), len(floor))

    # Add start
    start_x = int((len(floor[0]) - START_WIDTH) / 2)
    start_y = len(floor) - START_HEIGHT
    _Room(_RoomType.START).draw_to_blueprint(blueprint, openings, start_x, start_y)

    _place_rooms(blueprint, openings)

    _build_floor(blueprint, floor)
    start = int(len(floor[0]) / 2), len(floor) - 1
    return start


def _place_rooms(blueprint, openings):
    """Draw rooms to the blueprint of this floor, ensuring connectivity."""
    number_of_rooms = 0
    number_of_attempts = 0

    while number_of_rooms < MAX_ROOMS and number_of_attempts < MAX_ROOM_GENERATION_ATTEMPTS:
        room = _Room()

        conjunction_point = room.add_to_blueprint(blueprint, openings)
        if conjunction_point is not None:
            number_of_rooms += 1
        number_of_attempts += 1

        if ANIMATE_WORLD_GEN:
            _render_room(blueprint, openings, room, conjunction_point)


def _render_room(blueprint, openings, room, conjunction_point):
    # Draw the currently pending room
    blt.clear()
    room.render(ANIMATION_RENDERER)
    blt.bkcolor(blt.color_from_argb(255, 0, 0, 0))
    blt.refresh()
    time.sleep(ANIMATION_FRAME_LENGTH / 1000)

    # If it was added successfully, show the world with its new addition.
    if conjunction_point is not None:
        blt.clear()

        ANIMATION_CAMERA.move_to(conjunction_point[0], conjunction_point[1])
        ANIMATION_RENDERER.transform(ANIMATION_CAMERA)

        for y in range(len(blueprint)):
            for x in range(len(blueprint[0])):
                blueprint[y][x].render(x, y, ANIMATION_RENDERER)

        for (x, y) in openings:
            ANIMATION_RENDERER.render(x, y, Symbol(' ', blt.color_from_name("white")), 0, blt.color_from_argb(255, 0, 120, 0))
        blt.bkcolor(blt.color_from_argb(255, 0, 0, 0))
        blt.refresh()
        time.sleep(ANIMATION_FRAME_LENGTH / 1000)

        ANIMATION_CAMERA.move_to(0, 0)
        ANIMATION_RENDERER.transform(ANIMATION_CAMERA)


def _is_in_bounds(floor, x, y):
    """Determine if the given coordinates are within the bounds of the floor."""
    return 0 <= x < len(floor[0]) and 0 <= y < len(floor)


def _valid_placement_pos(blueprint, pos):
    x, y = pos[0], pos[1]
    if not _is_in_bounds(blueprint, x, y) or not blueprint[y][x].obstructed:
        return False
    for i in range(-1, 2, 2):
        if _is_in_bounds(blueprint, x, y + i) and not blueprint[y + i][x].obstructed:
            return False
        if _is_in_bounds(blueprint, x + i, y) and not blueprint[y][x + i].obstructed:
            return False
    return True


def _build_floor(blueprint, floor):
    """Build the floor using the given blueprint.  blueprint is a 2D array of GenTiles and floor is a 2D array of
    Tiles."""
    for i in range(len(blueprint)):
        for j in range(len(blueprint[0])):
            if not blueprint[j][i].obstructed:
                floor[j][i].unblock()
