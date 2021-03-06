# Base grid code from:
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame

import random
import sys
import pygame
from dataclasses import dataclass

MARGIN = 2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 500 + MARGIN
WINDOW_WIDTH = 500 + MARGIN
BLOCK_SIZE = 10

@dataclass
class Point:
    x: int
    y: int
    on: bool

def __init__(self, _x, _y, _on):
    x = _x
    y = _x
    on = _on

def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    grid = []
    points = []

    run_algo = False

    for x in range(0, WINDOW_WIDTH//BLOCK_SIZE):
        
        row = []

        for y in range(0, WINDOW_HEIGHT//BLOCK_SIZE):
            row.append(Point(x, y, False))

        grid.append(row)

    while True:

        if len(points) == 2 and run_algo:
            bresenham(points, grid)
            run_algo = False

        drawGrid(grid)
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                        
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    cell_x = mouse_x // BLOCK_SIZE
                    cell_y = mouse_y // BLOCK_SIZE
                    
                    pt = grid[cell_x][cell_y]
                    
                    if len(points) == 2:
                        old_pt = points.pop(0)
                    
                    points.append(pt)
                    pt.on = True

                    run_algo = True

                if mouse_presses[2]:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    cell_x = mouse_x // BLOCK_SIZE
                    cell_y = mouse_y // BLOCK_SIZE
                    
                    circle(grid, (cell_x, cell_y))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c:
                    clear_grid(grid)
                    points = []
        
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def clear_grid(grid):
    for row in grid:
        for pt in row:
            pt.on = False

def drawGrid(grid):
    for row in grid:
        for pt in row:
            rect = pygame.Rect((pt.x*BLOCK_SIZE)+MARGIN, (pt.y*BLOCK_SIZE)+MARGIN, BLOCK_SIZE-MARGIN, BLOCK_SIZE-MARGIN)
            
            color = BLACK if pt.on == True else WHITE

            pygame.draw.rect(SCREEN, color, rect)

def plot_line_low(points, grid):
    pt0, pt1 = points[0], points[1]
    dx = pt1.x - pt0.x
    dy = pt1.y - pt0.y
    yi = 1

    if dy < 0:
        yi = -1
        dy = -dy

    D = 2*dy - dx
    y = pt0.y

    for x in range(pt0.x, pt1.x):
        grid[x][y].on = True

        if D > 0:
            y += yi
            D += 2 * (dy - dx)
        else:
            D += 2*dy

def plot_line_high(points, grid):
    pt0, pt1 = points[0], points[1]
    dx = pt1.x - pt0.x
    dy = pt1.y - pt0.y
    xi = 1

    if dx < 0:
        xi = -1
        dx = -dx
    D = 2*dx - dy
    x = pt0.x

    for y in range(pt0.y, pt1.y):
        grid[x][y].on = True
        if D > 0:
            x += xi
            D += 2 * (dx - dy)
        else:
            D += 2*dx

def bresenham(points, grid):
    pt0, pt1 = points[0], points[1]

    dx = pt1.x - pt0.x
    dy = pt1.y - pt0.y

    if abs(dy) < abs(dx):
        if pt0.x > pt1.x:
            plot_line_low(list(reversed(points)), grid)
        else:
            plot_line_low(points, grid)
    else:
        if pt0.y > pt1.y:
            plot_line_high(list(reversed(points)), grid)
        else:
            plot_line_high(points, grid) 

# https://funloop.org/post/2021-03-15-bresenham-circle-drawing-algorithm.html
def mirror_points_8(x, y):
    """ Return 8-way symmetry of points. """
    return [( x,  y),
            ( y,  x),
            (-x,  y),
            (-y,  x),
            ( x, -y),
            ( y, -x),
            (-x, -y),
            (-y, -x)]

def circle(grid, center):
    y = random.randint(2, 6)
    x = 0
    d = 3 - (2 * y)

    for (ptx, pty) in mirror_points_8(x, y):
        grid[(center[0]+ptx) % len(grid[0])][(center[1]+pty) % len(grid)].on = True

    while (x < y):
        x+=1

        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10

        else:
            d += 4 * x + 6

        for (ptx, pty) in mirror_points_8(x, y):
            grid[(center[0]+ptx) % len(grid[0])][(center[1]+pty) % len(grid)].on = True

if __name__ == '__main__':
    main()
