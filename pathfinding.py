"""
PATHFINDING MODULE - Task 2 & Task 3 Implementation
Backend implementation for maze solving algorithms

This module provides:
- BFS (Breadth-First Search) algorithm
- Path reconstruction using backtracking
- Utility functions for grid operations
- Validation functions

Integration:
- Frontend (main.py) calls find_path_bfs()
- Backend returns (visited_nodes, final_path)
- Frontend animates the result

Author: Bouchra Hanini
Date: April 2026
"""

from typing import List, Tuple, Optional, Dict
from collections import deque
from enum import IntEnum


# ====== TYPE DEFINITIONS ======
class CellType(IntEnum):
    """Cell types for the maze grid"""
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3
    VISITED = 4
    FINAL_PATH = 5


# Type aliases for clarity
Coordinate = Tuple[int, int]  # (row, col)
Grid = List[List[int]]  # 2D grid
ParentMap = Dict[Coordinate, Optional[Coordinate]]  # For backtracking


# ============================================================
# TASK 2: PATHFINDING ALGORITHM IMPLEMENTATION
# ============================================================

def find_path_bfs(
    grid: Grid,
    start: Coordinate,
    end: Coordinate
) -> Tuple[List[Coordinate], List[Coordinate]]:
    """
    Find the shortest path using Breadth-First Search (BFS).
    
    BFS guarantees the shortest path in unweighted graphs.
    
    Args:
        grid (Grid): 2D grid matrix where:
            0 = empty cell
            1 = wall (obstacle)
            2 = start point
            3 = end point
        start (Coordinate): Starting position (row, col)
        end (Coordinate): Target position (row, col)
    
    Returns:
        Tuple[List[Coordinate], List[Coordinate]]: 
            - visited_nodes: All explored nodes in order of discovery
            - final_path: Shortest path from start to end
    
    Example:
        >>> grid = [
        ...     [0, 1, 0, 0],
        ...     [0, 1, 0, 1],
        ...     [0, 0, 0, 0],
        ... ]
        >>> visited, path = find_path_bfs(grid, (0, 0), (2, 3))
        >>> # visited = [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3)]
        >>> # path = [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3)]
    
    Algorithm Steps:
        1. Initialize queue with start position
        2. Track visited nodes for animation
        3. Explore neighbors in BFS order (4-directional)
        4. Store parent pointers for path reconstruction
        5. Return visited_nodes and reconstructed final_path
    
    Complexity:
        Time: O(rows × cols) - each cell visited once
        Space: O(rows × cols) - for queue and visited set
    """
    
    if not start or not end or not grid:
        return [], []
    
    rows, cols = len(grid), len(grid[0])
    
    # Validate start and end positions
    if not (0 <= start[0] < rows and 0 <= start[1] < cols):
        return [], []
    if not (0 <= end[0] < rows and 0 <= end[1] < cols):
        return [], []
    
    # Initialize data structures
    visited_set = {start}  # For O(1) lookup
    visited_nodes = [start]  # For animation (order matters)
    queue = deque([start])
    parent_map: ParentMap = {start: None}
    
    # BFS main loop
    found = False
    while queue and not found:
        current = queue.popleft()
        
        # Check if we reached the goal
        if current == end:
            found = True
            break
        
        # Explore all neighbors (4-directional: up, down, left, right)
        neighbors = get_neighbors(current[0], current[1], rows, cols, use_diagonals=False)
        
        for neighbor in neighbors:
            row, col = neighbor
            
            # Skip if already visited
            if neighbor in visited_set:
                continue
            
            # Skip if it's a wall
            if grid[row][col] == CellType.WALL:
                continue
            
            # Mark as visited and add to queue
            visited_set.add(neighbor)
            visited_nodes.append(neighbor)
            queue.append(neighbor)
            parent_map[neighbor] = current
    
    # Reconstruct path if goal was found
    if found:
        final_path = reconstruct_path(parent_map, start, end)
    else:
        final_path = []
        print("⚠️ No path found!")
    
    return visited_nodes, final_path


def find_path_astar(
    grid: Grid,
    start: Coordinate,
    end: Coordinate
) -> Tuple[List[Coordinate], List[Coordinate]]:
    """
    Find the shortest path using A* algorithm.
    
    A* is faster than BFS for single-target pathfinding because it uses
    a heuristic (Manhattan distance) to guide the search.
    
    Args:
        grid (Grid): 2D grid matrix
        start (Coordinate): Starting position (row, col)
        end (Coordinate): Target position (row, col)
    
    Returns:
        Tuple[List[Coordinate], List[Coordinate]]: (visited_nodes, final_path)
    
    Note:
        This is an optional enhancement. BFS is simpler and sufficient for
        this project. Implement only if time and performance allow.
    
    Complexity:
        Time: O(rows × cols) worst case, usually much faster
        Space: O(rows × cols)
    """
    # TODO: Implement A* algorithm
    # For now, fall back to BFS
    return find_path_bfs(grid, start, end)


# ============================================================
# TASK 3: PATH RECONSTRUCTION LOGIC
# ============================================================

def reconstruct_path(
    parent_map: ParentMap,
    start: Coordinate,
    end: Coordinate
) -> List[Coordinate]:
    """
    Reconstruct the shortest path using parent pointers.
    
    This function uses backtracking - starting from the end node and
    following parent pointers back to the start.
    
    Args:
        parent_map (ParentMap): Dictionary mapping each node to its parent
            Format: {(row, col): (parent_row, parent_col), ...}
        start (Coordinate): Starting position (row, col)
        end (Coordinate): Target position (row, col)
    
    Returns:
        List[Coordinate]: Ordered path from start to end
    
    Example:
        >>> parent_map = {
        ...     (0, 0): None,       # Start has no parent
        ...     (1, 0): (0, 0),     # Node (1,0) came from (0,0)
        ...     (2, 0): (1, 0),     # Node (2,0) came from (1,0)
        ...     (2, 1): (2, 0),     # Node (2,1) came from (2,0)
        ... }
        >>> path = reconstruct_path(parent_map, (0, 0), (2, 1))
        >>> # path = [(0,0), (1,0), (2,0), (2,1)]
    
    Algorithm:
        1. Start from end node
        2. Follow parent pointers backward to start
        3. Reverse the collected path
    
    Complexity:
        Time: O(path_length) - proportional to shortest path length
        Space: O(path_length) - for storing the path
    """
    
    path = []
    current = end
    
    # Backtrack from end to start
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = parent_map.get(current)
    
    # Reverse to get start-to-end order
    path.reverse()
    
    return path


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def get_neighbors(
    row: int,
    col: int,
    rows: int,
    cols: int,
    use_diagonals: bool = False
) -> List[Coordinate]:
    """
    Get valid neighbor cells for a given position.
    
    Args:
        row (int): Current row
        col (int): Current column
        rows (int): Total number of rows
        cols (int): Total number of columns
        use_diagonals (bool): If True, include diagonal neighbors
    
    Returns:
        List[Coordinate]: List of valid neighbor coordinates
    
    Examples:
        4-directional neighbors (default):
            up, down, left, right
        
        8-directional neighbors (with diagonals):
            up, down, left, right + 4 diagonals
    """
    neighbors = []
    
    # 4-directional movements: up, down, left, right
    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1),   # Right
    ]
    
    if use_diagonals:
        # Add diagonal movements
        directions += [
            (-1, -1),  # Up-left
            (-1, 1),   # Up-right
            (1, -1),   # Down-left
            (1, 1),    # Down-right
        ]
    
    # Check each direction
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        
        # Validate bounds
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))
    
    return neighbors


def is_walkable(grid: Grid, row: int, col: int) -> bool:
    """
    Check if a cell is walkable (not a wall).
    
    Args:
        grid (Grid): The maze grid
        row (int): Row coordinate
        col (int): Column coordinate
    
    Returns:
        bool: True if cell is not a wall, False otherwise
    """
    if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
        return False
    
    cell = grid[row][col]
    return cell != CellType.WALL


def heuristic(a: Coordinate, b: Coordinate) -> float:
    """
    Calculate Manhattan distance between two points.
    
    Used as heuristic for A* algorithm.
    
    Args:
        a (Coordinate): First point (row, col)
        b (Coordinate): Second point (row, col)
    
    Returns:
        float: Manhattan distance
    
    Formula:
        distance = |a.row - b.row| + |a.col - b.col|
    
    Note:
        Manhattan distance is admissible (never overestimates)
        and consistent, making it ideal for A*.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ============================================================
# VALIDATION & TESTING FUNCTIONS
# ============================================================

def validate_path(
    grid: Grid,
    path: List[Coordinate],
    start: Coordinate,
    end: Coordinate
) -> bool:
    """
    Validate that a path is valid and connects start to end.
    
    Checks:
        1. Path is not empty
        2. Path starts at start position
        3. Path ends at end position
        4. All consecutive cells are adjacent (Manhattan distance = 1)
        5. No cells in path are walls
    
    Args:
        grid (Grid): The maze grid
        path (List[Coordinate]): The path to validate
        start (Coordinate): Expected start position
        end (Coordinate): Expected end position
    
    Returns:
        bool: True if path is valid, False otherwise
    """
    # Check if path is empty
    if not path:
        return False
    
    # Check start and end
    if path[0] != start or path[-1] != end:
        return False
    
    # Check each step
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        
        r1, c1 = current
        r2, c2 = next_node
        
        # Check if cells are adjacent (Manhattan distance = 1)
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            return False
        
        # Check if next cell is a wall
        if grid[r2][c2] == CellType.WALL:
            return False
    
    return True


def test_pathfinding():
    """
    Basic test for pathfinding algorithm.
    
    Creates a simple maze and tests if algorithm finds a path.
    """
    # Create a simple 5x5 maze
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
    
    print("Test Pathfinding")
    print(f"Grid size: {len(test_grid)}x{len(test_grid[0])}")
    print(f"Start: {start}, End: {end}")
    print(f"Visited nodes: {len(visited)}")
    print(f"Path length: {len(path)}")
    print(f"Path: {path}")
    print(f"Valid: {validate_path(test_grid, path, start, end)}")
    
    return visited, path


# ============================================================
# INTEGRATION WITH FRONTEND
# ============================================================

"""
USAGE EXAMPLE - How Frontend (main.py) uses this module:

    from pathfinding import find_path_bfs, validate_path
    
    # When user presses SPACE in the UI:
    if event.key == pygame.K_SPACE:
        if maze.start_pos and maze.end_pos:
            try:
                # Call BFS algorithm
                visited_nodes, final_path = find_path_bfs(
                    maze.get_grid(),
                    maze.get_start_pos(),
                    maze.get_end_pos()
                )
                
                # Validate result
                if validate_path(maze.get_grid(), final_path, 
                               maze.get_start_pos(), maze.get_end_pos()):
                    # Set animation data
                    maze.set_visited_nodes(visited_nodes)
                    maze.set_path_nodes(final_path)
                    maze.start_animation()
                else:
                    print("❌ Path validation failed!")
            
            except Exception as e:
                print(f"Error during pathfinding: {e}")
        else:
            print("⚠️ Please set both START (S) and END (E)!")
"""


# ====== MAIN (for testing) ======
if __name__ == "__main__":
    print("=" * 50)
    print("PATHFINDING MODULE TEST")
    print("=" * 50)
    test_pathfinding()
    print("\nTest complete!")
