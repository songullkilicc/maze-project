import pygame
import random

pygame.init()

WIDTH, HEIGHT = 500, 500
ROWS = 10
CELL_SIZE = WIDTH // ROWS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

grid = [[0 for _ in range(ROWS)] for _ in range(ROWS)]

visited_nodes = []

def generate_fake_path():
    global visited_nodes
    visited_nodes = []

    for _ in range(30):
        r = random.randint(0, ROWS-1)
        c = random.randint(0, ROWS-1)
        if grid[r][c] == 0:
            visited_nodes.append((r, c))

running = True
animate = False
index = 0

while running:
    screen.fill(WHITE)

    for row in range(ROWS):
        for col in range(ROWS):
            color = WHITE

            if grid[row][col] == 1:
                color = BLACK
            elif grid[row][col] == 2:
                color = GREEN
            elif grid[row][col] == 3:
                color = RED
            elif grid[row][col] == 4:
                color = BLUE

            pygame.draw.rect(screen, color,
                (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (200,200,200),
                (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row = pos[1] // CELL_SIZE
            col = pos[0] // CELL_SIZE
            grid[row][col] = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                pos = pygame.mouse.get_pos()
                row = pos[1] // CELL_SIZE
                col = pos[0] // CELL_SIZE
                grid[row][col] = 2

            if event.key == pygame.K_e:
                pos = pygame.mouse.get_pos()
                row = pos[1] // CELL_SIZE
                col = pos[0] // CELL_SIZE
                grid[row][col] = 3

            if event.key == pygame.K_SPACE:
                generate_fake_path()
                animate = True
                index = 0

    if animate and index < len(visited_nodes):
        r, c = visited_nodes[index]
        if grid[r][c] == 0:
            grid[r][c] = 4
        index += 1
        pygame.time.delay(50)

    pygame.display.update()

pygame.quit()