from typing import List, Tuple, Optional, Dict
from collections import deque

# =========================
# TYPES
# =========================
Coordinate = Tuple[int, int]


# =========================
# MAZE CLASS (TASK 1)
# =========================
class Maze:
    """
    Backend Maze model
    Handles grid + start/end + reset logic
    """

    EMPTY = 0
    WALL = 1

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

        self.grid = [[self.EMPTY for _ in range(cols)] for _ in range(rows)]

        self.start: Optional[Coordinate] = None
        self.end: Optional[Coordinate] = None

    # ---------- SETTERS ----------

    def set_wall(self, x: int, y: int):
        if self._valid(x, y):
            self.grid[x][y] = self.WALL

    def remove_wall(self, x: int, y: int):
        if self._valid(x, y):
            self.grid[x][y] = self.EMPTY

    def set_start(self, x: int, y: int):
        if self._valid(x, y):
            self.start = (x, y)

    def set_end(self, x: int, y: int):
        if self._valid(x, y):
            self.end = (x, y)

    def reset(self):
        """Reset grid but keep start/end"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = self.EMPTY

    # ---------- HELPERS ----------

    def _valid(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols

    def get_grid(self):
        return self.grid


# =========================
# BFS (TASK 2)
# =========================
def bfs(maze: Maze):
    """
    Returns:
        visited_nodes (for animation)
        final_path (shortest path)
    """

    start = maze.start
    end = maze.end
    grid = maze.get_grid()

    if not start or not end:
        return [], []

    queue = deque([start])
    visited = set([start])
    parent: Dict[Coordinate, Optional[Coordinate]] = {start: None}

    visited_nodes = []
    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    found = False

    while queue:
        node = queue.popleft()
        visited_nodes.append(node)

        if node == end:
            found = True
            break

        x, y = node

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < maze.rows and
                0 <= ny < maze.cols and
                grid[nx][ny] != Maze.WALL and
                (nx, ny) not in visited
            ):
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = node

    final_path = []

    if found:
        cur = end
        while cur is not None:
            final_path.append(cur)
            cur = parent[cur]
        final_path.reverse()

    return visited_nodes, final_path


# =========================
# PATH RECONSTRUCTION (TASK 3)
# =========================
def reconstruct_path(
    parent: Dict[Coordinate, Optional[Coordinate]],
    start: Coordinate,
    end: Coordinate
):
    path = []
    current = end

    while current is not None:
        path.append(current)
        if current == start:
            break
        current = parent[current]

    return path[::-1]