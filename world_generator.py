from enum import Enum
from symbol import Symbol
from renderer import Renderer
from camera import Camera
import world
import utilities as util
import pathfinding
import colors
from bearlibterminal import terminal as blt
import random as rand
import math
import time

ANIMATE_WORLD_GEN = True
ANIMATION_FRAME_LENGTH = 250  # Measured in milliseconds
ANIMATION_RENDERER = Renderer()
ANIMATION_CAMERA = None

START_WIDTH = 11
START_HEIGHT = 6

MAX_ROOMS = 29  # Assume the start room has already been placed.
MAX_ROOM_GENERATION_ATTEMPTS = 250


class _GenTile:
    """A tile containing extra information needed strictly for world generation."""
    def __init__(self, blocked):
        self.blocked = blocked

    def render(self, x, y, renderer, bkcolor=None):
        """Render this tile at the given world coordinates."""
        if bkcolor is None:
            if self.blocked:
                color = colors.WALL
            else:
                color = colors.FLOOR
        else:
            color = bkcolor
        renderer.render(x, y, Symbol(' ', blt.color_from_name("white")), 0, color)


class _RoomType(Enum):
    """Enumerator cataloguing the different shapes of rooms."""
    RECTANGLE = 0
    CONJOINED_RECTANGLE = 1
    TORUS = 2
    START = 60
    RANDOM = 100

    @staticmethod
    def generic_rooms():
        """Returns a list of generic, non-unique room types, along with a weight."""
        return [(0.5, _RoomType.RECTANGLE), (0.4, _RoomType.CONJOINED_RECTANGLE), (0.1, _RoomType.TORUS)]


class _Room:
    """A set of points, with some being potential openings.  A in a room point exists on an abstract canvas, and only serve
    to provide relative positioning to other points."""
    RECTANGLE_WIDTH_RANGE = (6, 12)
    RECTANGLE_HEIGHT_RANGE = (5, 10)
    TORUS_INNER_RADIUS_RANGE = (1, 2)
    TORUS_RING_WIDTH_RANGE = (3, 6)

    def __init__(self, room_type=_RoomType.RANDOM):
        self.body = set()  # A set of points that make up this room.
        self.openings = set()  # A set containing the openings of this room.  self.body ∩ self.openings = ∅

        if room_type == _RoomType.RANDOM:
            weight = rand.random()
            weight_total = 0
            for room in _RoomType.generic_rooms():
                weight_total += room[0]
                if weight_total >= weight:
                    room_type = room[1]
                    break

        if room_type == _RoomType.RECTANGLE:
            width = rand.randint(self.RECTANGLE_WIDTH_RANGE[0], self.RECTANGLE_WIDTH_RANGE[1])
            height = rand.randint(self.RECTANGLE_HEIGHT_RANGE[0], self.RECTANGLE_HEIGHT_RANGE[1])
            self.__add_rectangle(0, 0, width, height)
        elif room_type == _RoomType.CONJOINED_RECTANGLE:
            # Draw first rectangle
            width = rand.randint(self.RECTANGLE_WIDTH_RANGE[0], self.RECTANGLE_WIDTH_RANGE[1])
            height = rand.randint(self.RECTANGLE_HEIGHT_RANGE[0], self.RECTANGLE_HEIGHT_RANGE[1])
            self.__add_rectangle(0, 0, width, height)
            # Draw a second, overlapping rectangle
            second_width = rand.randint(self.RECTANGLE_WIDTH_RANGE[0], self.RECTANGLE_WIDTH_RANGE[1])
            second_height = rand.randint(self.RECTANGLE_HEIGHT_RANGE[0], self.RECTANGLE_HEIGHT_RANGE[1])
            x = rand.randint(-second_width + 1, width - 1)
            y = rand.randint(-second_height + 1, height - 1)
            self.__add_rectangle(x, y, second_width, second_height)
        elif room_type == _RoomType.TORUS:
            inner_radius = rand.randint(self.TORUS_INNER_RADIUS_RANGE[0], self.TORUS_INNER_RADIUS_RANGE[1])
            ring_width = rand.randint(self.TORUS_RING_WIDTH_RANGE[0], self.TORUS_RING_WIDTH_RANGE[1])
            self.__add_torus(inner_radius, ring_width)

        elif room_type == _RoomType.START:
            self.__add_start()

    def __add_rectangle(self, x, y, width, height):
        """Overlap a rectangle starting at the given coordinates to this room."""
        for i in range(y, y + height):
            for j in range(x, x + width):
                self.body.add((j, i))
                if (j, i) in self.openings: self.openings.remove((j, i))

        # Remove any openings that may be covered by this rectangle
        for p in self.openings:
            if p in self.body:
                self.openings.remove(p)

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

    def __add_torus(self, inner_radius, ring_width):
        for y in range(inner_radius + ring_width + 2):
            for x in range(inner_radius + ring_width + 2):
                if inner_radius ** 2 < x ** 2 + y ** 2 < (inner_radius + ring_width) ** 2:
                    self.body.add((x, y))
                    self.body.add((-x, y))
                    self.body.add((x, -y))
                    self.body.add((-x, -y))
        # Add openings
        # Top / bottom side
        min_inner, max_inner = int(-inner_radius), int(inner_radius)
        min_outer, max_outer = int(-inner_radius/2 - ring_width), int(inner_radius/2 + ring_width)
        exit_pos = (rand.randint(min_inner, max_inner), min_outer - 1)
        if exit_pos not in self.body: self.openings.add(exit_pos)
        exit_pos = (rand.randint(min_inner, max_inner), max_outer + 1)
        if exit_pos not in self.body: self.openings.add(exit_pos)

        # Left / right side
        exit_pos = (min_outer - 1, rand.randint(min_inner, max_inner))
        if exit_pos not in self.body: self.openings.add(exit_pos)
        exit_pos = (max_outer + 1, rand.randint(min_inner, max_inner))
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
                # Translate each tile of the body to the real world, and check that they are all a valid cell for placement.
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
        blueprint[world_opening[1]][world_opening[0]].blocked = False
        world_openings.remove(world_opening)
        self.draw_to_blueprint(blueprint, world_openings, world_opening[0] - room_opening[0], world_opening[1] - room_opening[1])

    def draw_to_blueprint(self, blueprint, openings, x, y):
        """Assumes no overlap between blueprint and T(x, y)(self.body), where T is the translation function.  Updates openings to reflect room addition."""
        for (p1, p2) in self.body:
            blueprint[p2 + y][p1 + x].blocked = False
            for o in [(o1, o2) for (o1, o2) in openings if o1 == p1 and o2 == p2]:
                openings.remove(o)

        for (p1, p2) in self.openings:
            # Some openings may be obstructed since they lie outside of this.body
            if util.is_in_bounds(blueprint, p1 + x, p2 + y) and blueprint[p2 + y][p1 + x].blocked:
                openings.add((p1 + x, p2 + y))

    def render(self, renderer):
        for tile in self.body:
            renderer.render(10 + tile[0], 5 + tile[1], Symbol(' ', blt.color_from_name("white")), 0, colors.WORLD_GEN_HIGHLIGHT)
        for opening in self.openings:
            renderer.render(10 + opening[0], 5 + opening[1], Symbol('V', blt.color_from_name("white")), 0, colors.WORLD_GEN_OPENING)


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
    start_y = len(floor) - START_HEIGHT - 1
    _Room(_RoomType.START).draw_to_blueprint(blueprint, openings, start_x, start_y)

    _place_rooms(blueprint, openings)
    _place_cycles(blueprint)
    _pad_edges(blueprint)
    blueprint[45][39].blocked = True
    blueprint[47][41].blocked = True

    _build_floor(blueprint, floor)
    start = int(len(floor[0]) / 2), len(floor) - 2
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


def _place_cycles(blueprint):
    """Place cycles in the world."""
    minimum_acyclic_distance = 50
    for (x, y) in [(x, y) for y in range(len(blueprint)) for x in range(len(blueprint[0]))]:
        if blueprint[y][x].blocked:
            if util.is_in_bounds(blueprint, x - 1, y) and not blueprint[y][x - 1].blocked and util.is_in_bounds(blueprint, x + 1, y) and not blueprint[y][x + 1].blocked:
                n = pathfinding.pathing_distance(blueprint, (x - 1, y), (x + 1, y))
                if n.distance > minimum_acyclic_distance:
                    if ANIMATE_WORLD_GEN:
                        _render_cycle(blueprint, n.to_path())
                    blueprint[y][x].blocked = False
            if util.is_in_bounds(blueprint, x, y - 1) and not blueprint[y - 1][x].blocked and util.is_in_bounds(blueprint, x, y + 1) and not blueprint[y + 1][x].blocked:
                n = pathfinding.pathing_distance(blueprint, (x, y - 1), (x, y + 1))
                if n.distance > minimum_acyclic_distance:
                    if ANIMATE_WORLD_GEN:
                        _render_cycle(blueprint, n.to_path())
                    blueprint[y][x].blocked = False


def _pad_edges(blueprint):
    """Pad the edges of the floor with walls, ensuring that there are no floor tiles adjacent to the edge of the world."""
    x_max, y_max = len(blueprint[0]), len(blueprint)
    for y in range(y_max):
        blueprint[y][0].blocked = True
        blueprint[y][x_max - 1].blocked = True
    for x in range(x_max):
        blueprint[0][x].blocked = True
        blueprint[y_max - 1][x].blocked = True


def _render_room(blueprint, openings, room, conjunction_point):
    # Draw the currently pending room
    blt.clear()
    room.render(ANIMATION_RENDERER)
    blt.bkcolor(colors.CLEAR)
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
            ANIMATION_RENDERER.render(x, y, Symbol(' ', blt.color_from_name("white")), 0, colors.WORLD_GEN_OPENING)
        blt.bkcolor(colors.CLEAR)
        blt.refresh()
        time.sleep(ANIMATION_FRAME_LENGTH / 1000)

        ANIMATION_CAMERA.move_to(0, 0)
        ANIMATION_RENDERER.transform(ANIMATION_CAMERA)


def _render_cycle(blueprint, path):
    blt.clear()
    ANIMATION_CAMERA.move_to(path[0][0], path[0][1])
    ANIMATION_RENDERER.transform(ANIMATION_CAMERA)

    for y in range(len(blueprint)):
        for x in range(len(blueprint[0])):
            blueprint[y][x].render(x, y, ANIMATION_RENDERER)

    for (x, y) in path:
        ANIMATION_RENDERER.render(x, y, Symbol(' ', blt.color_from_name("white")), 0, colors.WORLD_GEN_CYCLE)

    blt.bkcolor(colors.CLEAR)
    blt.refresh()
    time.sleep(ANIMATION_FRAME_LENGTH / 1000)

    ANIMATION_CAMERA.move_to(0, 0)
    ANIMATION_RENDERER.transform(ANIMATION_CAMERA)


def _valid_placement_pos(blueprint, pos):
    x, y = pos[0], pos[1]
    if not util.is_in_bounds(blueprint, x, y) or not blueprint[y][x].blocked:
        return False
    for i in range(-1, 2, 2):
        if util.is_in_bounds(blueprint, x, y + i) and not blueprint[y + i][x].blocked:
            return False
        if util.is_in_bounds(blueprint, x + i, y) and not blueprint[y][x + i].blocked:
            return False
        if util.is_in_bounds(blueprint, x + i, y - 1) and not blueprint[y - 1][x + i].blocked:
            return False
        if util.is_in_bounds(blueprint, x + i, y + 1) and not blueprint[y + 1][x + i].blocked:
            return False
    return True


def _build_floor(blueprint, floor):
    """Build the floor using the given blueprint.  blueprint is a 2D array of GenTiles and floor is a 2D array of
    Tiles."""
    for i in range(len(blueprint)):
        for j in range(len(blueprint[0])):
            if not blueprint[i][j].blocked:
                floor[i][j].unblock()
