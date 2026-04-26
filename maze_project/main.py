# MAZE PATHFINDING PROJECT - Task 1 & 3: GUI & VISUALIZATION ENGINE
# Frontend Implementation by Songül Kılıç
# 
# DESCRIPTION:
# This file contains the complete frontend implementation including:
# - Grid rendering system
# - Mouse/keyboard input handling
# - Animation engine for pathfinding visualization
# 
# FEATURES:
# - Draw/erase walls with mouse drag
# - Set start (S) and end (E) points
# - Animate pathfinding algorithm
# - Configurable animation speed with F/G keys
# - Clear maze with C key

import pygame
from enum import IntEnum

pygame.init()

# ====== CONFIGURATION ======
class CellType(IntEnum):
    """Cell types for the maze grid"""
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3
    VISITED = 4
    FINAL_PATH = 5


class Colors:
    """Color palette for the visualization"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)      # Start point
    RED = (255, 0, 0)        # End point
    BLUE = (100, 100, 255)
    GRAY = (200, 200, 200)   # Grid lines
    LIGHT_BLUE = (173, 216, 230)  # Visited nodes
    YELLOW = (255, 255, 0)   # Final path
    DARK_BLUE = (70, 130, 180)    # Alternative for visited


# ====== GAME CONFIGURATION ======
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS
FPS = 60

# ====== ANIMATION CONFIGURATION ======
DEFAULT_ANIMATION_SPEED = 50  # milliseconds per frame
MIN_ANIMATION_SPEED = 10
MAX_ANIMATION_SPEED = 200


# ====== MAZE VISUALIZATION CLASS ======
class MazeVisualizer:
    """
    Main class for maze visualization and pathfinding animation.
    
    Manages:
    - Grid rendering and cell management
    - User input (mouse and keyboard)
    - Animation playback
    - Integration with pathfinding backend
    """
    
    def __init__(self, rows, cols, cell_size):
        """
        Initialize the maze visualizer.
        
        Args:
            rows (int): Number of rows in grid
            cols (int): Number of columns in grid
            cell_size (int): Size of each cell in pixels
        """
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size
        self.height = rows * cell_size
        
        # Grid matrix: 0=empty, 1=wall, 2=start, 3=end, 4=visited, 5=final_path
        self.grid = [[CellType.EMPTY for _ in range(cols)] for _ in range(rows)]
        
        # Special positions
        self.start_pos = None
        self.end_pos = None
        
        # Animation system
        self.visited_nodes = []
        self.final_path = []
        self.animating = False
        self.animation_index = 0
        self.animation_speed = DEFAULT_ANIMATION_SPEED
        self.last_animation_time = 0
        
        # Drawing mode (for drag-and-draw)
        self.drawing = False
        
        # Pygame setup
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(
            "Maze Pathfinding Solver - Draw maze (drag), S=Start, E=End, SPACE=Animate, F=Slower, G=Faster, C=Clear"
        )
        self.clock = pygame.time.Clock()
        
        # Font for text display
        self.font = pygame.font.Font(None, 24)
    
    # ====== GRID MANAGEMENT ======
    
    def screen_to_grid(self, pos):
        """
        Convert screen pixel coordinates to grid coordinates.
        
        Args:
            pos (tuple): Screen coordinates (x, y)
            
        Returns:
            tuple: Grid coordinates (row, col) or None if out of bounds
        """
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None
    
    def set_cell(self, row, col, cell_type):
        """
        Set a cell to a specific type with proper state management.
        
        Args:
            row (int): Row coordinate
            col (int): Column coordinate
            cell_type (CellType): Type to set the cell to
        """
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
    
    # ====== DRAWING ======
    
    def draw_grid(self):
        """
        Draw the entire maze grid with current state.
        Renders each cell with appropriate color based on its type.
        """
        self.screen.fill(Colors.WHITE)
        
        for row in range(self.rows):
            for col in range(self.cols):
                cell_type = self.grid[row][col]
                x = col * self.cell_size
                y = row * self.cell_size
                
                # Determine color based on cell type
                if cell_type == CellType.WALL:
                    color = Colors.BLACK
                elif cell_type == CellType.START:
                    color = Colors.GREEN
                elif cell_type == CellType.END:
                    color = Colors.RED
                elif cell_type == CellType.VISITED:
                    color = Colors.LIGHT_BLUE
                elif cell_type == CellType.FINAL_PATH:
                    color = Colors.YELLOW
                else:
                    color = Colors.WHITE
                
                # Draw cell rectangle
                pygame.draw.rect(self.screen, color, 
                               (x, y, self.cell_size, self.cell_size))
                
                # Draw grid lines
                pygame.draw.rect(self.screen, Colors.GRAY,
                               (x, y, self.cell_size, self.cell_size), 1)
        
        # Draw status information
        self._draw_status()
        
        pygame.display.update()
    
    def _draw_status(self):
        """Draw status text on screen."""
        status_text = []
        
        if self.animating:
            status_text.append(f"Searching... ({self.animation_index}/{len(self.visited_nodes)})")
        elif self.animation_index > 0:
            status_text.append("Animation complete!")
        else:
            status_text.append("Ready. Draw maze, set S & E, press SPACE")
        
        status_text.append(f"Speed: {self.animation_speed}ms (F=slower, G=faster)")
        
        y_offset = 10
        for text in status_text:
            surf = self.font.render(text, True, Colors.BLACK)
            self.screen.blit(surf, (10, y_offset))
            y_offset += 25
    
    # ====== INPUT HANDLING ======
    
    def handle_events(self):
        """
        Handle all pygame events (mouse, keyboard, window).
        
        Returns:
            bool: False if quit event, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Mouse button down - start drawing
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.drawing = True
                self._handle_mouse_draw(pygame.mouse.get_pos())
            
            # Mouse button up - stop drawing
            if event.type == pygame.MOUSEBUTTONUP:
                self.drawing = False
            
            # Mouse motion - continue drawing (drag-and-draw)
            if event.type == pygame.MOUSEMOTION and self.drawing:
                self._handle_mouse_draw(pygame.mouse.get_pos())
            
            # Keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    # Set start point
                    pos = pygame.mouse.get_pos()
                    coords = self.screen_to_grid(pos)
                    if coords:
                        row, col = coords
                        self.set_cell(row, col, CellType.START)
                
                elif event.key == pygame.K_e:
                    # Set end point
                    pos = pygame.mouse.get_pos()
                    coords = self.screen_to_grid(pos)
                    if coords:
                        row, col = coords
                        self.set_cell(row, col, CellType.END)
                
                elif event.key == pygame.K_SPACE:
                    # Start animation
                    if self.start_pos and self.end_pos:
                        self.start_animation()
                    else:
                        print("⚠️  Please set both START (S) and END (E) positions!")
                
                elif event.key == pygame.K_c:
                    # Clear grid
                    self.clear_grid()
                
                elif event.key == pygame.K_f:
                    # Slow down animation
                    self.animation_speed = min(MAX_ANIMATION_SPEED, self.animation_speed + 10)
                    print(f"Animation speed: {self.animation_speed}ms per frame")
                
                elif event.key == pygame.K_g:
                    # Speed up animation
                    self.animation_speed = max(MIN_ANIMATION_SPEED, self.animation_speed - 10)
                    print(f"Animation speed: {self.animation_speed}ms per frame")
        
        return True
    
    def _handle_mouse_draw(self, pos):
        """
        Handle mouse drawing (toggle walls).
        
        Args:
            pos (tuple): Mouse position (x, y)
        """
        coords = self.screen_to_grid(pos)
        if coords:
            row, col = coords
            # Toggle wall (draw or erase)
            if self.grid[row][col] == CellType.WALL:
                self.set_cell(row, col, CellType.EMPTY)
            elif self.grid[row][col] == CellType.EMPTY:
                self.set_cell(row, col, CellType.WALL)
    
    # ====== ANIMATION ======
    
    def start_animation(self):
        """
        Begin animation sequence.
        Should be called when user presses SPACE.
        """
        self.animating = True
        self.animation_index = 0
        self.last_animation_time = pygame.time.get_ticks()
        print("✓ Animation started! (waiting for pathfinding data)")
    
    def update_animation(self):
        """
        Update animation state (called each frame).
        Animates the visited nodes one by one with configurable speed.
        """
        if not self.animating or not self.visited_nodes:
            return
        
        current_time = pygame.time.get_ticks()
        
        # Check if enough time has passed for next frame
        if current_time - self.last_animation_time >= self.animation_speed:
            if self.animation_index < len(self.visited_nodes):
                row, col = self.visited_nodes[self.animation_index]
                
                # Only color empty cells (don't overwrite start/end)
                if self.grid[row][col] == CellType.EMPTY:
                    self.grid[row][col] = CellType.VISITED
                
                self.animation_index += 1
                self.last_animation_time = current_time
            else:
                # All visited nodes displayed, now show final path
                if self.final_path and self.animation_index == len(self.visited_nodes):
                    self._display_final_path()
                    self.animation_index += 1
                else:
                    # Animation complete
                    self.animating = False
                    print("✓ Animation complete! Path found.")
    
    def _display_final_path(self):
        """Display the final shortest path in yellow."""
        for row, col in self.final_path:
            if self.grid[row][col] == CellType.VISITED:
                self.grid[row][col] = CellType.FINAL_PATH
    
    def clear_grid(self):
        """Clear all walls and animations but keep start/end points."""
        self.visited_nodes = []
        self.final_path = []
        self.animating = False
        self.animation_index = 0
        
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] not in [CellType.START, CellType.END]:
                    self.grid[row][col] = CellType.EMPTY
    
    # ====== BACKEND INTEGRATION INTERFACE ======
    
    def set_visited_nodes(self, nodes):
        """
        INTERFACE METHOD: Backend (Task 2) sets visited nodes here.
        
        Args:
            nodes (list): List of (row, col) tuples in discovery order
        """
        self.visited_nodes = nodes
    
    def set_path_nodes(self, path):
        """
        INTERFACE METHOD: Backend (Task 3) sets final path nodes here.
        
        Args:
            path (list): List of (row, col) tuples from start to end
        """
        self.final_path = path
    
    def get_grid(self):
        """
        INTERFACE METHOD: Backend retrieves grid here.
        
        Returns:
            list: 2D grid representing the maze
        """
        return self.grid
    
    def get_start_pos(self):
        """Get start position for backend."""
        return self.start_pos
    
    def get_end_pos(self):
        """Get end position for backend."""
        return self.end_pos
    
    # ====== MAIN LOOP ======
    
    def run(self):
        """
        Main game loop.
        Renders, handles input, and updates animation continuously.
        """
        running = True
        
        while running:
            self.draw_grid()
            running = self.handle_events()
            self.update_animation()
            self.clock.tick(FPS)
        
        pygame.quit()


# ====== MAIN ENTRY POINT ======
if __name__ == "__main__":
    # Create and run the maze visualizer
    maze = MazeVisualizer(ROWS, COLS, CELL_SIZE)
    maze.run()
