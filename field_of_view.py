import utilities as util


def get_fov_map(floor, origin, sight_radius):
    fov_map = [(origin[0], origin[1])]
    for i in [-1, 1]:
        # Quadrants 1 and 6
        quadrant = [[(origin[0] + x, origin[1] - y * i) for x in range(-y, 1)] for y in range(1, sight_radius)]
        fov_map.extend(_generate_fov_map(floor, quadrant, origin, 1, False, 1, 0))
        # Quadrants 2 and 5
        quadrant = [[(origin[0] - x, origin[1] - y * i) for x in range(-y, 1)] for y in range(1, sight_radius)]
        fov_map.extend(_generate_fov_map(floor, quadrant, origin, 1, False, 1, 0))
        # Quadrants 7 and 4
        quadrant = [[(origin[0] - x * i, origin[1] - y) for y in range(-x, 1)] for x in range(1, sight_radius)]
        fov_map.extend(_generate_fov_map(floor, quadrant, origin, 1, True, 1, 0))
        # Quadrants 8 and 3
        quadrant = [[(origin[0] - x * i, origin[1] + y) for y in range(-x, 1)] for x in range(1, sight_radius)]
        fov_map.extend(_generate_fov_map(floor, quadrant, origin, 1, True, 1, 0))
    return fov_map


def _generate_fov_map(floor, quadrant, origin, depth, rotated, start_slope, end_slope):
    """Recursive shadowcasting algorithm, detailed at: http://www.roguebasin.com/index.php?title=FOV_using_recursive_shadowcasting"""
    (origin_x, origin_y) = origin
    if depth == len(quadrant):
        return []

    fov_map = []
    local_start_slope, local_end_slope = start_slope, end_slope
    end_changed = False
    for cell_x in (cell_x for cell_x in range(len(quadrant[depth - 1])) if depth - int(round(depth * start_slope)) <= cell_x <= depth - int(round(depth * end_slope))):
        (x, y) = quadrant[depth - 1][cell_x]
        # Update local start/end slope depending on the whether the current tile is blocked.
        if util.is_in_bounds(floor, x, y):
            fov_map.append((x, y))
            rise = abs(origin_y - y) if rotated else abs(origin_x - x)
            if not floor[y][x].blocked:
                local_end_slope = rise / depth
                end_changed = True
            else:
                if end_changed:
                    fov_map.extend(
                        _generate_fov_map(floor, quadrant, origin, depth + 1, rotated, local_start_slope, local_end_slope))
                    end_changed = False
                local_start_slope = rise / (depth + 1)
    if end_changed:
        fov_map.extend(
            _generate_fov_map(floor, quadrant, origin, depth + 1, rotated, local_start_slope, local_end_slope))
    return fov_map




