import pygame
from enum import IntEnum

pygame.init()

# ====== CONFIGURATION ======
class CellType(IntEnum):
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3
    VISITED = 4

class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (100, 100, 255)
    GRAY = (200, 200, 200)
    LIGHT_BLUE = (173, 216, 230)

# ====== GAME CONFIGURATION ======
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS
FPS = 60

# ====== MAZE VISUALIZATION CLASS ======
class MazeVisualizer:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size
        self.height = rows * cell_size
        
        # Grid matrix: 0=empty, 1=wall, 2=start, 3=end, 4=visited
        self.grid = [[CellType.EMPTY for _ in range(cols)] for _ in range(rows)]
        
        # Special positions
        self.start_pos = None
        self.end_pos = None
        
        # Animation
        self.visited_nodes = []
        self.animating = False
        self.animation_index = 0
        self.animation_speed = 50  # milliseconds between frames
        self.last_animation_time = 0
        
        # Drawing mode
        self.drawing = False
        self.erase_mode = False
        
        # Initialize pygame window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Solver - Draw maze, press SPACE to start")
        self.clock = pygame.time.Clock()
    
    def screen_to_grid(self, pos):
        """Convert screen coordinates to grid coordinates"""
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None
    
    def set_cell(self, row, col, cell_type):
        """Set a cell to a specific type, handling conflicts"""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        
        if cell_type == CellType.START:
            # Remove old start position
            if self.start_pos:
                old_row, old_col = self.start_pos
                self.grid[old_row][old_col] = CellType.EMPTY
            self.start_pos = (row, col)
            self.grid[row][col] = CellType.START
            
        elif cell_type == CellType.END:
            # Remove old end position
            if self.end_pos:
                old_row, old_col = self.end_pos
                self.grid[old_row][old_col] = CellType.EMPTY
            self.end_pos = (row, col)
            self.grid[row][col] = CellType.END
            
        else:
            self.grid[row][col] = cell_type
    
    def draw_grid(self):
        """Draw the grid and all cells"""
        self.screen.fill(Colors.WHITE)
        
        for row in range(self.rows):
            for col in range(self.cols):
                cell_type = self.grid[row][col]
                x = col * self.cell_size
                y = row * self.cell_size
                
                # Choose color based on cell type
                if cell_type == CellType.WALL:
                    color = Colors.BLACK
                elif cell_type == CellType.START:
                    color = Colors.GREEN
                elif cell_type == CellType.END:
                    color = Colors.RED
                elif cell_type == CellType.VISITED:
                    color = Colors.LIGHT_BLUE
                else:
                    color = Colors.WHITE
                
                # Draw cell
                pygame.draw.rect(self.screen, color, 
                               (x, y, self.cell_size, self.cell_size))
                # Draw grid lines
                pygame.draw.rect(self.screen, Colors.GRAY,
                               (x, y, self.cell_size, self.cell_size), 1)
        
        pygame.display.update()
    
    def handle_events(self):
        """Handle all input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.drawing = True
                pos = pygame.mouse.get_pos()
                coords = self.screen_to_grid(pos)
                if coords:
                    row, col = coords
                    # Toggle wall (draw/erase)
                    if self.grid[row][col] == CellType.WALL:
                        self.set_cell(row, col, CellType.EMPTY)
                    else:
                        self.set_cell(row, col, CellType.WALL)
            
            if event.type == pygame.MOUSEBUTTONUP:
                self.drawing = False
            
            if event.type == pygame.MOUSEMOTION and self.drawing:
                # Click and drag functionality
                pos = pygame.mouse.get_pos()
                coords = self.screen_to_grid(pos)
                if coords:
                    row, col = coords
                    if self.grid[row][col] == CellType.WALL:
                        self.set_cell(row, col, CellType.EMPTY)
                    else:
                        self.set_cell(row, col, CellType.WALL)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    # Place START point
                    pos = pygame.mouse.get_pos()
                    coords = self.screen_to_grid(pos)
                    if coords:
                        row, col = coords
                        self.set_cell(row, col, CellType.START)
                
                if event.key == pygame.K_e:
                    # Place END point
                    pos = pygame.mouse.get_pos()
                    coords = self.screen_to_grid(pos)
                    if coords:
                        row, col = coords
                        self.set_cell(row, col, CellType.END)
                
                if event.key == pygame.K_SPACE:
                    # Start animation (will receive visited_nodes from backend)
                    if self.start_pos and self.end_pos:
                        self.start_animation()
                    else:
                        print("⚠️  Please set both START (S) and END (E) positions!")
                
                if event.key == pygame.K_c:
                    # Clear the grid
                    self.clear_grid()
        
        return True
    
    def clear_grid(self):
        """Clear all walls but keep start/end"""
        self.visited_nodes = []
        self.animating = False
        
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] not in [CellType.START, CellType.END]:
                    self.grid[row][col] = CellType.EMPTY
    
    def start_animation(self):
        """Begin animation sequence"""
        self.animating = True
        self.animation_index = 0
        self.last_animation_time = pygame.time.get_ticks()
        # visited_nodes will be populated by backend (Task 2 & 3)
        print("✓ Animation ready! (Waiting for pathfinding algorithm)")
    
    def update_animation(self):
        """Update animation frame"""
        if not self.animating or not self.visited_nodes:
            return
        
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_animation_time >= self.animation_speed:
            if self.animation_index < len(self.visited_nodes):
                row, col = self.visited_nodes[self.animation_index]
                # Only color empty cells (don't overwrite start/end)
                if self.grid[row][col] == CellType.EMPTY:
                    self.grid[row][col] = CellType.VISITED
                
                self.animation_index += 1
                self.last_animation_time = current_time
            else:
                # Animation complete
                self.animating = False
                print("✓ Animation complete!")
    
    def set_visited_nodes(self, nodes):
        """INTERFACE METHOD: Backend sets visited nodes here"""
        self.visited_nodes = nodes
    
    def set_path_nodes(self, path):
        """INTERFACE METHOD: Backend sets final path nodes here"""
        for row, col in path:
            if self.grid[row][col] == CellType.VISITED:
                self.grid[row][col] = CellType.VISITED  # Keep blue, or use different color
    
    def get_grid(self):
        """INTERFACE METHOD: Backend retrieves grid here"""
        return self.grid
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            self.draw_grid()
            running = self.handle_events()
            self.update_animation()
            self.clock.tick(FPS)
        
        pygame.quit()

# ====== MAIN ======
if __name__ == "__main__":
    maze = MazeVisualizer(ROWS, COLS, CELL_SIZE)
    maze.run()
