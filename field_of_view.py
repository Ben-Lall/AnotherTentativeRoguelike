import math


def get_fov_map(floor, origin, sight_radius):
    return _generate_fov_map(floor, origin, sight_radius, 0, 1, 0)


def _generate_fov_map(floor, origin, sight_radius, depth, start_slope, end_slope):
    """Recursive shadowcasting algorithm, detailed at: http://www.roguebasin.com/index.php?title=FOV_using_recursive_shadowcasting"""
    (row_x, row_y) = origin
    if row_y < 0 or row_y > len(floor):
        return []

    in_view = []
    for x in (_ for _ in range(row_x - int(round(depth * start_slope)), 1 + row_x - int(round(depth * end_slope))) if 0 < _ < len(floor[0])):
        if not floor[row_y][x].blocked:
            in_view.append((x, row_y))
        #else:

