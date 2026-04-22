"""
PATHFINDING MODULE - Task 2 & 3
Bouchra'nın bu fonksiyonları implement etmesi gerekir

Bu module Front-End (Songül) ve Back-End (Bouchra) arasında
iletişim sağlar.
"""

from typing import List, Tuple, Optional
from collections import deque
from enum import IntEnum

class CellType(IntEnum):
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3
    VISITED = 4

# Tip tanımları (clarity için)
Coordinate = Tuple[int, int]  # (row, col)
Grid = List[List[int]]

# ============================================================
# TASK 2: PATHFINDING ALGORITHM IMPLEMENTATION
# ============================================================

def find_path_bfs(
    grid: Grid,
    start: Coordinate,
    end: Coordinate
) -> Tuple[List[Coordinate], List[Coordinate]]:
    """
    TASK 2 - Bouchra bunu implement edecek
    
    BFS (Breadth-First Search) algoritması ile en kısa yolu bul.
    
    Args:
        grid: 2D grid matrisi (0=empty, 1=wall, 2=start, 3=end, 4=visited)
        start: Başlangıç koordinatları (row, col)
        end: Bitiş koordinatları (row, col)
    
    Returns:
        tuple: (visited_nodes, final_path)
            - visited_nodes: Keşfedilen tüm nodes (animasyon için)
            - final_path: Başlangıçtan bitişe en kısa yol
    
    Örnek kullanım:
        visited, path = find_path_bfs(grid, (0, 0), (9, 9))
        # visited = [(0,0), (0,1), (1,1), (1,2), ...]
        # path = [(0,0), (0,1), (0,2), (1,2), (2,2), ..., (9,9)]
    
    İmplementasyon adımları:
    1. Queue başlat, start noktasını ekle
    2. visited_nodes boş liste başlat (animasyon için)
    3. Köşegen + 4-yönlü hareket yapılabilir (8-directional da olabilir)
    4. visited_nodes'a keşfedilen nodes'u sırasıyla ekle
    5. TASK 3 için parent pointers kaydet → final path reconstruct et
    """
    pass  # Bouchra implement edecek


def find_path_astar(
    grid: Grid,
    start: Coordinate,
    end: Coordinate
) -> Tuple[List[Coordinate], List[Coordinate]]:
    """
    TASK 2 - Alternatif: Bouchra A* yapmak isterse
    
    A* (A-Star) algoritması ile heuristic-optimized yol bul.
    
    Args:
        grid: 2D grid matrisi
        start: Başlangıç koordinatları
        end: Bitiş koordinatları
    
    Returns:
        tuple: (visited_nodes, final_path)
    
    A* BFS'ten daha hızlı olabilir çünkü heuristic kullanır.
    Ancak BFS implementation'ı daha basit olduğundan,
    eğer zaman darlığı varsa BFS'e devam et.
    """
    pass  # Opsiyonel


# ============================================================
# TASK 3: PATH RECONSTRUCTION LOGIC
# ============================================================

def reconstruct_path(
    parent_pointers: dict,
    start: Coordinate,
    end: Coordinate
) -> List[Coordinate]:
    """
    TASK 3 - Bouchra bunu implement edecek
    
    Backtracking mantığı: Parent pointers kullanarak
    Start'dan End'e en kısa yolu geri çıkar.
    
    Args:
        parent_pointers: {(row, col): (parent_row, parent_col), ...}
            Keşif sırasında her node'un kime ulaştığını tutar
        start: Başlangıç noktası
        end: Bitiş noktası
    
    Returns:
        List[Coordinate]: End'den Start'a giden koordinatlar
    
    Örnek:
        parent_pointers = {
            (0,1): (0,0),
            (1,1): (0,1),
            (1,2): (1,1),
            (2,2): (1,2),
        }
        path = reconstruct_path(parent_pointers, (0,0), (2,2))
        # path = [(2,2), (1,2), (1,1), (0,1), (0,0)]
        # ya da reverse et: [(0,0), (0,1), (1,1), (1,2), (2,2)]
    
    İmplementasyon adımları:
    1. current = end ile başla
    2. while current != start:
        - path'e current ekle
        - current = parent_pointers[current]
    3. start'ı path'e ekle
    4. path'i ters çevir (end → start yerine start → end)
    """
    path = []
    current = end
    
    while current is not None and current != start:
        path.append(current)
        current = parent_pointers.get(current)
    
    path.append(start)
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
    Bir hücrenin komşu hücrelerini döndür
    
    Args:
        row, col: Hücre konumu
        rows, cols: Grid boyutu
        use_diagonals: True ise 8-directional (köşegenli),
                      False ise 4-directional (ortagonal)
    
    Returns:
        List[(row, col), ...]: Geçerli komşu koordinatları
    """
    neighbors = []
    
    # 4-directional: up, down, left, right
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    if use_diagonals:
        # 8-directional: yukarıdaki + diagonal
        directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))
    
    return neighbors


def is_walkable(grid: Grid, row: int, col: int) -> bool:
    """
    Bir hücre yürünebilir mi? (duvar değilse)
    """
    if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
        return False
    
    cell = grid[row][col]
    # Duvar değilse yürünebilir
    return cell != CellType.WALL


def heuristic(a: Coordinate, b: Coordinate) -> float:
    """
    Manhattan distance: A* için heuristic fonksiyon
    
    Args:
        a, b: Koordinatlar (row, col)
    
    Returns:
        Manhattan distance
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ============================================================
# TEST & VALIDATION
# ============================================================

def validate_path(
    grid: Grid,
    path: List[Coordinate],
    start: Coordinate,
    end: Coordinate
) -> bool:
    """
    Path'in valid olup olmadığını kontrol et
    
    Kontroller:
    - Path'in başı start'ta mı?
    - Path'in sonu end'de mi?
    - Yol sürekli (ardışık koordinatlar) mi?
    - Hiç duvar üzerinde geçmiş mi?
    """
    if not path:
        return False
    
    if path[0] != start or path[-1] != end:
        return False
    
    for i in range(len(path) - 1):
        r1, c1 = path[i]
        r2, c2 = path[i + 1]
        
        # İki nokta komşu mu?
        if abs(r1 - r2) + abs(c1 - c2) > 2:  # Manhattan distance
            return False
        
        # Duvar üzerinde geçmiş mi?
        if grid[r2][c2] == CellType.WALL:
            return False
    
    return True


# ============================================================
# INTEGRATION ÖRNEK (Front-End Task 1'den kullanılacak)
# ============================================================

"""
main.py'de (Task 1) kullanım:

from pathfinding import find_path_bfs, validate_path

# User SPACE'e bastı, animasyon başla
if event.key == pygame.K_SPACE:
    # Back-end (Task 2) çağır
    visited_nodes, final_path = find_path_bfs(
        maze.grid,
        maze.start_pos,
        maze.end_pos
    )
    
    # Validate
    if validate_path(maze.grid, final_path, maze.start_pos, maze.end_pos):
        # Front-end'e set et
        maze.set_visited_nodes(visited_nodes)
        maze.set_path_nodes(final_path)
    else:
        print("❌ Path calculation failed!")
"""
