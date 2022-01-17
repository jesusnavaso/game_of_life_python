__author__ = "Jesús Navas Orozco"

"""
Conway's Game of Life.
Cellular automaton made with pygame
"""
import sys
import tkinter as tk
import pygame
from pygame.surface import Surface

import colors
from cell import Cell


def create_background():
    grid = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    grid.fill(colors.WHITE)
    draw_grid(grid)
    # pygame.image.save(grid, "./resources/background_horizontal_toolbar.png")
    return grid


def determine_status_by_neighbours(cell: Cell, neighbours: int):
    if not cell.status and neighbours == 3:
        cell.status = True
    if cell.status and (neighbours == 2 or neighbours == 3):
        pass
    else:
        cell.status = False


def draw_counter(generation_counter: int, screen):
    # my_rect = pygame.Rect(0, WINDOW_HEIGHT, TOOLBAR_PIXEL_SIZE, TOOLBAR_PIXEL_SIZE)
    # pygame.display.update(pygame.draw.rect(screen, colors.BLUE, my_rect))
    my_font = pygame.font.SysFont("Arial", 20)
    counter_text = my_font.render("Generation:", True, colors.BLACK)
    counter = my_font.render("# " + str(generation_counter), True, colors.BLACK)
    screen.blit(counter_text, (0, WINDOW_HEIGHT - TOOLBAR_PIXEL_SIZE))
    screen.blit(counter, (0, WINDOW_HEIGHT - TOOLBAR_PIXEL_SIZE + 20))


def draw_current_universe(currently_alive_cells: set[Cell], window, cell_size: int):
    for cell in currently_alive_cells:
        cell_rect = pygame.Rect(cell.x_pos * cell_size, cell.y_pos * cell_size, cell_size, cell_size)
        pygame.draw.rect(window, colors.BLACK, cell_rect)


def draw_grid(screen):
    for coordinate_pair in grid_coordinates:
        pygame.draw.line(screen, color=colors.GRAY, start_pos=coordinate_pair[0], end_pos=coordinate_pair[1],
                         width=2)


def error_checking():
    """ERROR CHECKING for pygame
    pygame.init() import the modules necessary for pygame to work. It returns a tuple (a,b), where a is
    the number of correctly imported modules and b is the number of modules imported with errors"""
    check_errors = pygame.init()

    if check_errors[1] > 0:
        print(f'[!] {check_errors[1]} have not been imported correctly, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')


def get_neighbours(cell: Cell):
    x, y = cell.x_pos, cell.y_pos

    # We cannot get outside our universe of cells: 0 <= x <= n_cells_x-1, 0 <= y <= n_cells_y-1,
    x1 = max(x - 1, 0)
    y1 = max(y - 1, 0)
    x2 = min(x + 1, n_cells_x - 1)
    y2 = min(y + 1, n_cells_y - 1)

    # Use set structure to avoid repeated cells
    neighbours_positions = {(x1, y1), (x1, y), (x1, y2), (x, y1), (x, y2), (x2, y1), (x2, y), (x2, y2)} - {(x, y)}

    return {Cell(status=False, x_pos=a, y_pos=b) for a, b in neighbours_positions}


def get_next_generation(currently_alive_cells: set[Cell]):
    new_candidates = currently_alive_cells
    for cell in currently_alive_cells:
        new_candidates = new_candidates.union(get_neighbours(cell))
    for cell in new_candidates:
        determine_status_by_neighbours(cell,
                                       get_number_of_alive_neighbours(neighbours=get_neighbours(cell),
                                                                      currently_alive_cells=currently_alive_cells))

    return set(filter(lambda x: x.status, new_candidates))


def get_number_of_alive_neighbours(neighbours: set[Cell], currently_alive_cells: set[Cell]):
    return sum(map(lambda x: x in currently_alive_cells, neighbours))


def set_initial_state(x_cells: int, y_cells: int):
    center_x, center_y = (round(x_cells / 2), round(y_cells / 2))
    initial_alive_cells_positions = {(center_x, center_y), (center_x, center_y - 1), (center_x, center_y + 1),
                                     (center_x - 1, center_y - 1), (center_x + 1, center_y)}
    return {Cell(x_pos=x, y_pos=y, status=True) for x, y in initial_alive_cells_positions}


def main():
    icon = pygame.image.load('./resources/icon.png')
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    alive_cells = set_initial_state(n_cells_x, n_cells_y)
    pygame.display.set_caption('Game of Life')
    # background_image = pygame.image.load("./resources/background.png").convert()
    background_image = create_background()
    generation_counter = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # screen.fill(colors.WHITE)
        # To correct a slight displacement of the image background
        screen.blit(background_image, [-1, -1])
        draw_current_universe(currently_alive_cells=alive_cells, window=screen, cell_size=BLOCK_SIZE)
        draw_counter(generation_counter, screen)
        pygame.display.update()
        alive_cells = get_next_generation(currently_alive_cells=alive_cells)
        generation_counter += 1
        generation_clock.tick(refresh_rate)


if __name__ == '__main__':
    error_checking()
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    WINDOW_WIDTH = min(720, width)
    WINDOW_HEIGHT = min(480, height)
    TOOLBAR_WIDTH = 5  # In cells
    BLOCK_SIZE = 10
    TOOLBAR_PIXEL_SIZE = TOOLBAR_WIDTH * BLOCK_SIZE

    generation_clock = pygame.time.Clock()
    refresh_rate = 60

    n_cells_x = int(WINDOW_WIDTH / BLOCK_SIZE)
    n_cells_y = int(WINDOW_HEIGHT / BLOCK_SIZE) - TOOLBAR_WIDTH

    # grid_coordinates
    grid_coordinates_x = [((a * BLOCK_SIZE, 0), (a * BLOCK_SIZE, WINDOW_HEIGHT - TOOLBAR_PIXEL_SIZE)) for a in
                          range(n_cells_x + 1)]
    grid_coordinates_y = [((0, b * BLOCK_SIZE), (WINDOW_WIDTH, b * BLOCK_SIZE)) for b in range(n_cells_y + 1)]
    grid_coordinates = grid_coordinates_x + grid_coordinates_y

    main()
