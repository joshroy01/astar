import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("a* path finding algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = list()
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE
        
    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE
        
    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = GREY

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors.clear()
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def reconstruct_path(came_from, end, draw):
    end.make_path()
    curr = end
    print(len(came_from))
    while curr in came_from:
        curr = came_from[curr]
        curr.make_path()
        draw()

def h(s1, s2):
    x1, y1 = s1
    x2, y2 = s2
    return abs(x1 - x2) + abs(y1 - y2)

def astar(draw, grid, start, end):
    count = 0
    openq = PriorityQueue()
    openq.put((0, count, start))
    came_from = dict()
    g = {spot: float('inf') for row in grid for spot in row}
    g[start] = 0
    f = {spot: float('inf') for row in grid for spot in row}
    f[start] = h(start.get_pos(), end.get_pos())
    
    openset = {start}

    while not openq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = openq.get()[2]
        openset.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g = g[current] + 1

            if temp_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in openset:
                    count += 1
                    openq.put((f[neighbor], count, neighbor))
                    openset.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current != start:
            current.make_closed()

    return False

def greedy(draw, grid, start, end):
    count = 0
    openq = PriorityQueue()
    openq.put((0, count, start))
    came_from = dict()
    v = {spot: float('inf') for row in grid for spot in row}
    
    openset = {start}

    while not openq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = openq.get()[2]
        openset.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in openset and not neighbor.is_closed():
                came_from[neighbor] = current
                v[neighbor] = h(neighbor.get_pos(), end.get_pos())
                count += 1
                openq.put((v[neighbor], count, neighbor))
                openset.add(neighbor)
                neighbor.make_open()
        
        draw()
        
        print('yo')
        current.make_closed()
        draw()

    return False

def make_grid(rows, width):
    grid = list()
    square = width // rows
    for i in range(rows):
        grid.append(list())
        for j in range(rows):
            spot = Spot(i, j, square, rows)
            grid[i].append(spot)
    return grid

def draw_grid(window, rows, width):
    square = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * square), (width, i * square))
        for j in range(rows):
            pygame.draw.line(window, GREY, (j * square, 0), (j * square, width))
        
def draw(window, grid, rows, width):
    window.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()


def get_click_pos(pos, rows, width):
    square = width // rows
    y, x = pos

    row = y // square
    col = x // square
    return row, col

def main(window, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            pos = pygame.mouse.get_pos()
            row, col = get_click_pos(pos, ROWS, width)
            spot = grid[row][col]

            if pygame.mouse.get_pressed()[0]:
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != start and spot != end:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]:
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    
                    astar(lambda: draw(window, grid, ROWS, width), grid, start, end)
                
                if event.key == pygame.K_g and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    
                    greedy(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_r:
                    for row in grid:
                        for spot in row:
                            spot.reset()
                    start = None
                    end = None



    pygame.quit()

main(WINDOW, WIDTH)