"""
PATHFINDING MODULE - Task 2 & Task 3 Implementation
+ Steps computation added
"""

from typing import List, Tuple, Optional, Dict
from collections import deque
from enum import IntEnum


# ====== TYPE DEFINITIONS ======
class CellType(IntEnum):
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3
    VISITED = 4
    FINAL_PATH = 5


Coordinate = Tuple[int, int]
Grid = List[List[int]]
ParentMap = Dict[Coordinate, Optional[Coordinate]]


# ============================================================
# BFS
# ============================================================

def find_path_bfs(
    grid: Grid,
    start: Coordinate,
    end: Coordinate
) -> Tuple[List[Coordinate], List[Coordinate]]:

    if not start or not end or not grid:
        return [], []

    rows, cols = len(grid), len(grid[0])

    if not (0 <= start[0] < rows and 0 <= start[1] < cols):
        return [], []
    if not (0 <= end[0] < rows and 0 <= end[1] < cols):
        return [], []

    visited_set = {start}
    visited_nodes = [start]
    queue = deque([start])
    parent_map: ParentMap = {start: None}

    found = False

    while queue and not found:
        current = queue.popleft()

        if current == end:
            found = True
            break

        neighbors = get_neighbors(current[0], current[1], rows, cols)

        for neighbor in neighbors:
            r, c = neighbor

            if neighbor in visited_set:
                continue

            if grid[r][c] == CellType.WALL:
                continue

            visited_set.add(neighbor)
            visited_nodes.append(neighbor)
            queue.append(neighbor)
            parent_map[neighbor] = current

    if found:
        final_path = reconstruct_path(parent_map, start, end)
    else:
        final_path = []
        print("⚠️ No path found!")

    return visited_nodes, final_path


# ============================================================
# PATH RECONSTRUCTION
# ============================================================

def reconstruct_path(
    parent_map: ParentMap,
    start: Coordinate,
    end: Coordinate
) -> List[Coordinate]:

    path = []
    current = end

    while current is not None:
        path.append(current)
        if current == start:
            break
        current = parent_map.get(current)

    path.reverse()
    return path


# ============================================================
# 🔥 NEW: STEPS FUNCTION
# ============================================================

def compute_steps(path: List[Coordinate]) -> int:
    """
    Steps = number of moves between nodes
    """
    if not path:
        return 0
    return len(path) - 1


# ============================================================
# UTILS
# ============================================================

def get_neighbors(row, col, rows, cols):
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    neighbors = []

    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))

    return neighbors


# ============================================================
# VALIDATION
# ============================================================

def validate_path(grid, path, start, end):

    if not path:
        return False

    if path[0] != start or path[-1] != end:
        return False

    for i in range(len(path) - 1):
        r1, c1 = path[i]
        r2, c2 = path[i+1]

        if abs(r1 - r2) + abs(c1 - c2) != 1:
            return False

        if grid[r2][c2] == CellType.WALL:
            return False

    return True


# ============================================================
# TEST
# ============================================================

def test_pathfinding():

    test_grid = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
    ]

    start = (0, 0)
    end = (4, 4)

    visited, path = find_path_bfs(test_grid, start, end)

    steps = compute_steps(path)

    print("=" * 50)
    print("PATHFINDING TEST")
    print("=" * 50)
    print(f"Visited nodes: {len(visited)}")
    print(f"Path length: {len(path)}")
    print(f"Steps (moves): {steps}")  # 👈 IMPORTANT
    print(f"Path: {path}")
    print(f"Valid: {validate_path(test_grid, path, start, end)}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    test_pathfinding()