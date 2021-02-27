import pygame
import random

GREY = (200, 200, 200)
WHITE = (255, 255, 255)
RED = (255, 0, 0, 200)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
height = 801
width = 1100
w = 20
pygame.font.init()
global grid

WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze creator in Python")
GRID_SURF = pygame.surface.Surface((801, 801))
pygame.draw.rect(WIN, GREY, (900, 200, 100, 50))
pygame.draw.rect(WIN, GREY, (900, 300, 100, 50))

my_font = pygame.font.SysFont('Calibri', 35)
text_surface = my_font.render('Start', False, (0, 0, 0))
WIN.blit(text_surface, (916, 209))
text_surface2 = my_font.render('Reset', False, (0, 0, 0))
WIN.blit(text_surface2, (910, 309))


def setup():
    global current, cols, rows, stack, grid
    stack = []
    grid = []

    cols = 800 // w
    rows = 800 // w

    for j in range(rows):
        for i in range(cols):
            node = Node(i, j)
            grid.append(node)

    current = grid[0]
    for i in range(len(grid)):
        grid[i].show()


def draw():
    global current, stack, play, grid
    GRID_SURF.fill(WHITE)
    for i in range(len(grid)):
        grid[i].show()

    current.visited = True
    current.highlight()
    next_one = current.check_neighbors()
    if next_one is not None:
        next_one.visited = True
        stack.append(current)
        remove_walls(current, next_one)
        current = next_one
    elif len(stack) > 0:
        current = stack.pop(len(stack) - 1)
    elif len(stack) == 0:
        play = False
        current.clear_highlight()


def index(i, j):
    if i < 0 or j < 0 or i > cols - 1 or j > rows - 1:
        return False
    return i + j * cols


class Node:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True, True, True, True]
        self.visited = False

    def check_neighbors(self):
        neighbors = []

        top = grid[index(self.i, self.j - 1)]
        right = grid[index(self.i + 1, self.j)]
        bottom = grid[index(self.i, self.j + 1)]
        left = grid[index(self.i - 1, self.j)]

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        if len(neighbors) > 0:
            r = random.randint(0, len(neighbors) - 1)
            return neighbors[r]
        else:
            return None

    def highlight(self):
        x = self.i * w
        y = self.j * w
        pygame.draw.rect(GRID_SURF, RED, (x+1, y+1, w, w))  # (50, 168, 115)

    def clear_highlight(self):
        x = self.i * w
        y = self.j * w
        pygame.draw.rect(GRID_SURF, WHITE, (x+1, y+1, w, w))

    def show(self):
        x = self.i * w
        y = self.j * w
        if self.walls[0]:
            # Make a line with (x, y, x+w, y)
            pygame.draw.line(GRID_SURF, BLACK, (x, y), (x+w, y))
        if self.walls[1]:
            # Make a line with (x+w, y, x+w, y+w)
            pygame.draw.line(GRID_SURF, BLACK, (x+w, y), (x+w, y+w))
        if self.walls[2]:
            # Make a line with (x+w, y+w, x, y+w)
            pygame.draw.line(GRID_SURF, BLACK, (x+w, y+w), (x, y+w))
        if self.walls[3]:
            # Make a line with (x, y+w, x, y)
            pygame.draw.line(GRID_SURF, BLACK, (x, y+w), (x, y))

        if self.visited:
            # Mark as Visited (change the color)
            # pygame.draw.rect(WIN, (87, 87, 87), (x+1, y+1, w-1, w-1))
            pass


def remove_walls(a, b):
    x = a.i - b.i
    if x == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif x == -1:
        a.walls[1] = False
        b.walls[3] = False

    y = a.j - b.j
    if y == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif y == -1:
        a.walls[2] = False
        b.walls[0] = False
        pass


def main():
    global play
    pygame.init()
    GRID_SURF.fill(WHITE)
    setup()
    play = False

    while True:
        WIN.blit(GRID_SURF, (0, 0))
        pygame.display.update()
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 900 < mouse_pos[0] < 1000 and 200 < mouse_pos[1] < 250:
                    play = True
                if 900 < mouse_pos[0] < 1000 and 300 < mouse_pos[1] < 350:
                    if not play:
                        setup()

        if play:
            draw()


if __name__ == '__main__':
    main()
