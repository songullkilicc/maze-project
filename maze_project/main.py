# MAZE PATHFINDING PROJECT - GUI WITH STEPS DISPLAY

import pygame
from enum import IntEnum
from maze_logic import Maze, bfs

pygame.init()

# ====== CONFIGURATION ======
class CellType(IntEnum):
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3
    VISITED = 4
    FINAL_PATH = 5


class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    LIGHT_BLUE = (173, 216, 230)
    YELLOW = (255, 255, 0)
    GRAY = (200, 200, 200)


WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS
FPS = 60

DEFAULT_ANIMATION_SPEED = 50
MIN_ANIMATION_SPEED = 10
MAX_ANIMATION_SPEED = 200


class MazeVisualizer:

    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size
        self.height = rows * cell_size

        self.grid = [[CellType.EMPTY for _ in range(cols)] for _ in range(rows)]

        self.start_pos = None
        self.end_pos = None

        self.visited_nodes = []
        self.final_path = []

        self.animating = False
        self.animation_index = 0
        self.animation_speed = DEFAULT_ANIMATION_SPEED
        self.last_animation_time = 0

        self.drawing = False

        # 🔥 NEW
        self.steps = 0

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Solver - SPACE to run")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

    # ====== STEPS ======
    def compute_steps(self, path):
        if not path:
            return 0
        return len(path) - 1

    # ====== GRID ======
    def screen_to_grid(self, pos):
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None

    def set_cell(self, row, col, cell_type):
        if cell_type == CellType.START:
            if self.start_pos:
                r, c = self.start_pos
                self.grid[r][c] = CellType.EMPTY
            self.start_pos = (row, col)

        elif cell_type == CellType.END:
            if self.end_pos:
                r, c = self.end_pos
                self.grid[r][c] = CellType.EMPTY
            self.end_pos = (row, col)

        self.grid[row][col] = cell_type

    # ====== DRAW ======
    def draw_grid(self):
        self.screen.fill(Colors.WHITE)

        for r in range(self.rows):
            for c in range(self.cols):
                x = c * self.cell_size
                y = r * self.cell_size

                cell = self.grid[r][c]

                if cell == CellType.WALL:
                    color = Colors.BLACK
                elif cell == CellType.START:
                    color = Colors.GREEN
                elif cell == CellType.END:
                    color = Colors.RED
                elif cell == CellType.VISITED:
                    color = Colors.LIGHT_BLUE
                elif cell == CellType.FINAL_PATH:
                    color = Colors.YELLOW
                else:
                    color = Colors.WHITE

                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, Colors.GRAY, (x, y, self.cell_size, self.cell_size), 1)

        self._draw_status()
        pygame.display.update()

    def _draw_status(self):
        status = []

        if self.animating:
            status.append("Searching...")
        else:
            status.append("Ready")

        status.append(f"Steps: {self.steps}")  # 🔥 NEW
        status.append(f"Speed: {self.animation_speed}ms")

        y = 10
        for text in status:
            surf = self.font.render(text, True, Colors.BLACK)
            self.screen.blit(surf, (10, y))
            y += 25

    # ====== EVENTS ======
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.drawing = True
                self._draw_wall(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONUP:
                self.drawing = False

            if event.type == pygame.MOUSEMOTION and self.drawing:
                self._draw_wall(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_s:
                    pos = self.screen_to_grid(pygame.mouse.get_pos())
                    if pos:
                        self.set_cell(*pos, CellType.START)

                elif event.key == pygame.K_e:
                    pos = self.screen_to_grid(pygame.mouse.get_pos())
                    if pos:
                        self.set_cell(*pos, CellType.END)

                elif event.key == pygame.K_SPACE:
                    if self.start_pos and self.end_pos:

                        maze = Maze(self.rows, self.cols)

                        for r in range(self.rows):
                            for c in range(self.cols):
                                if self.grid[r][c] == CellType.WALL:
                                    maze.set_wall(r, c)

                        maze.set_start(*self.start_pos)
                        maze.set_end(*self.end_pos)

                        visited, path = bfs(maze)

                        self.visited_nodes = visited
                        self.final_path = path

                        # 🔥 NEW
                        self.steps = self.compute_steps(path)
                        print(f"Steps: {self.steps}")

                        self.start_animation()

                elif event.key == pygame.K_c:
                    self.clear_grid()

                elif event.key == pygame.K_f:
                    self.animation_speed = min(MAX_ANIMATION_SPEED, self.animation_speed + 10)

                elif event.key == pygame.K_g:
                    self.animation_speed = max(MIN_ANIMATION_SPEED, self.animation_speed - 10)

        return True

    def _draw_wall(self, pos):
        coords = self.screen_to_grid(pos)
        if coords:
            r, c = coords
            if self.grid[r][c] == CellType.EMPTY:
                self.grid[r][c] = CellType.WALL
            elif self.grid[r][c] == CellType.WALL:
                self.grid[r][c] = CellType.EMPTY

    # ====== ANIMATION ======
    def start_animation(self):
        self.animating = True
        self.animation_index = 0
        self.last_animation_time = pygame.time.get_ticks()

    def update_animation(self):
        if not self.animating:
            return

        now = pygame.time.get_ticks()

        if now - self.last_animation_time >= self.animation_speed:

            if self.animation_index < len(self.visited_nodes):
                r, c = self.visited_nodes[self.animation_index]

                if self.grid[r][c] == CellType.EMPTY:
                    self.grid[r][c] = CellType.VISITED

                self.animation_index += 1
                self.last_animation_time = now

            else:
                for r, c in self.final_path:
                    if self.grid[r][c] == CellType.VISITED:
                        self.grid[r][c] = CellType.FINAL_PATH

                self.animating = False

    # ====== RESET ======
    def clear_grid(self):
        self.visited_nodes = []
        self.final_path = []
        self.animating = False
        self.animation_index = 0

        # 🔥 NEW
        self.steps = 0

        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] not in [CellType.START, CellType.END]:
                    self.grid[r][c] = CellType.EMPTY

    # ====== LOOP ======
    def run(self):
        running = True
        while running:
            self.draw_grid()
            running = self.handle_events()
            self.update_animation()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    app = MazeVisualizer(ROWS, COLS, CELL_SIZE)
    app.run()