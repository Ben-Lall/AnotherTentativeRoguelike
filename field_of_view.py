import math
import utilities as util


def get_fov_map(floor, origin, sight_radius):
    fov_map = [(origin[0], origin[1])]
    quadrant = [[x for x in range(origin[0] - y, origin[0] + 1) if util.is_in_bounds(floor, x, y)] for y in range(1, sight_radius)]
    fov_map.extend(_generate_fov_map(floor, quadrant, origin, 1, 1, 0))
    return fov_map


def _generate_fov_map(floor, quadrant, origin, depth, start_slope, end_slope):
    """Recursive shadowcasting algorithm, detailed at: http://www.roguebasin.com/index.php?title=FOV_using_recursive_shadowcasting"""
    row_x = origin[0]
    row_y = origin[1] - depth
    if row_y < 0 or row_y > len(floor) or depth == len(quadrant):
        return []

    fov_map = []
    local_start_slope, local_end_slope = start_slope, end_slope
    end_changed = False
    for cell_x in (_ for _ in range(row_x - int(round(depth * start_slope)), 1 + row_x - int(round(depth * end_slope))) if 0 <= _ < len(floor[0])):
        (x, y) = quadrant[row_y][cell_x]
        if not floor[y][x].blocked:
            fov_map.append((x, y))
            local_end_slope = (row_x - x) / depth
            end_changed = True
        else:
            if end_changed:
                fov_map.extend(
                    _generate_fov_map(floor, quadrant, origin, depth + 1, local_start_slope, local_end_slope))
                end_changed = False
            local_start_slope = (row_x - x) / (depth + 1)
    if end_changed:
        fov_map.extend(
            _generate_fov_map(floor, quadrant, origin, depth + 1, local_start_slope, local_end_slope))
    return fov_map




