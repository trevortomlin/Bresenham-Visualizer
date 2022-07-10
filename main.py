# Base grid code from:
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame

import sys
import pygame
from dataclasses import dataclass

MARGIN = 2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 500 + MARGIN
WINDOW_WIDTH = 500 + MARGIN
BLOCK_SIZE = 20

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

    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        
        row = []

        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            row.append(Point(x, y, False))

        grid.append(row)


    while True:
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
                        old_pt.on = False
                    
                    points.append(pt)
                    pt.on = True

                        

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def drawGrid(grid):
    for row in grid:
        for pt in row:
            rect = pygame.Rect(pt.x+MARGIN, pt.y+MARGIN, BLOCK_SIZE-MARGIN, BLOCK_SIZE-MARGIN)
            
            color = BLACK if pt.on == True else WHITE

            pygame.draw.rect(SCREEN, color, rect)

if __name__ == '__main__':
    main()
