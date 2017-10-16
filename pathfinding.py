import utilities as util
import heapq


class _AStarNode:
    def __init__(self, x, y, distance, h, parent):
        self.x = x
        self.y = y
        self.distance = distance
        self.h = h
        self.priority = distance + h
        self.parent = parent

    def __lt__(self, other):
        if self.priority < other.priority:
            return True
        elif self.priority > other.priority:
            return False
        else:
            if self.distance <= other.distance:
                return True
            else:
                return False

    def to_path(self):
        n = self
        path = [(n.x, n.y)]
        while n.parent is not None:
            n = n.parent
            path.insert(0, (n.x, n.y))
        return path


def pathing_distance(floor, start, target):
    sx, sy = start[0], start[1]
    expanded = [[False for x in range(len(floor[0]))] for y in range(len(floor))]
    start_node = _AStarNode(sx, sy, 0, util.euc_distance(start, target), None)
    h = [start_node]
    while len(h) > 0:
        e = heapq.heappop(h)
        if e.x == target[0] and e.y == target[1]:
            return e
        if not expanded[e.y][e.x]:
            expanded[e.y][e.x] = True
            for i in range(-1, 2, 2):
                if util.is_in_bounds(floor, e.x, e.y + i) and not floor[e.y + i][e.x].blocked and not expanded[e.y + i][e.x]:
                    n = _AStarNode(e.x, e.y + i, e.distance + 1, util.euc_distance((e.x, e.y + i), target), e)
                    heapq.heappush(h, n)
                if util.is_in_bounds(floor, e.x + i, e.y) and not floor[e.y][e.x + i].blocked and not expanded[e.y][e.x + i]:
                    n = _AStarNode(e.x + i, e.y, e.distance + 1, util.euc_distance((e.x + i, e.y), target), e)
                    heapq.heappush(h, n)
                if util.is_in_bounds(floor, e.x + i, e.y - 1) and not floor[e.y - 1][e.x + i].blocked and not expanded[e.y - 1][e.x + i]:
                    n = _AStarNode(e.x + i, e.y - 1, e.distance + 1.414, util.euc_distance((e.x + i, e.y - 1), target), e)
                    heapq.heappush(h, n)
                if util.is_in_bounds(floor, e.x + i, e.y + 1) and not floor[e.y + 1][e.x + i].blocked and not expanded[e.y + 1][e.x + i]:
                    n = _AStarNode(e.x + i, e.y + 1, e.distance + 1.414, util.euc_distance((e.x + i, e.y + 1), target), e)
                    heapq.heappush(h, n)
