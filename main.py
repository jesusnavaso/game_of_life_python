__author__ = "Jesús Navas Orozco"

import copy
import datetime

"""
Conway's Game of Life.
Cellular automaton made with pygame
"""
import pygame
import sys
from cell import Cell
import colors


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


def draw_game_window(window):
    pass


def set_initial_state(x_cells: int, y_cells: int):

    center_x, center_y = (round(x_cells / 2), round(y_cells / 2))
    initially_alive_cells = [(center_x, center_y), (center_x, center_y - 1), (center_x, center_y + 1),
                             (center_x - 1, center_y - 1), (center_x + 1, center_y)]

    initial_universe = [[Cell(status=(x, y) in initially_alive_cells, x_pos=x, y_pos=y) for x in range(x_cells)]
                        for y in range(y_cells)]

    return initial_universe


def draw_current_universe(current_universe, window, cell_size):
    for row in current_universe:
        for cell in row:
            cell_rect = pygame.Rect(cell.x_pos * cell_size, cell.y_pos * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface=window, color=colors.GRAY, rect=cell_rect, width=1)
            if cell.status:
                pygame.draw.rect(window, colors.BLACK, cell_rect)


def get_status_of_cell_by_position(x: int, y: int, universe):
    try:
        this_cell = universe[y][x]
        return this_cell.status
    except IndexError:
        print(f"Cell at ({x},{y}) is out of the universe.")


def get_number_of_neighbours(cell: Cell, universe):
    x, y = cell.x_pos, cell.y_pos

    # We cannot get outside our universe of cells: 0 <= x <= n_cells_x-1, 0 <= y <= n_cells_y-1,
    x1 = max(x-1, 0)
    y1 = max(y-1, 0)
    x2 = min(x + 1, n_cells_x-1)
    y2 = min(y + 1, n_cells_y-1)

    # Use set structure to avoid repeated cells
    neighbours_positions = {(x1, y1), (x1, y), (x1, y2), (x, y1), (x, y2), (x2, y1), (x2, y), (x2, y2)} - {(x, y)}

    return sum([get_status_of_cell_by_position(a, b, universe) for a, b in neighbours_positions])


def determine_status_by_neighbours(cell: Cell, neighbours: int):
    if not cell.status and neighbours == 3:
        cell.status = True
    if cell.status and (neighbours == 2 or neighbours == 3):
        pass
    else:
        cell.status = False


def get_next_generation(universe):
    new_generation = copy.deepcopy(universe)
    for row in new_generation:
        for cell in row:
            determine_status_by_neighbours(cell, get_number_of_neighbours(cell, universe))
    return new_generation


def main():
    game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    universe = set_initial_state(n_cells_x, n_cells_y)
    pygame.display.set_caption('Game of Life')
    count = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        game_window.fill(colors.WHITE)
        draw_current_universe(current_universe=universe, window=game_window, cell_size=block_size)
        pygame.display.update()
        # pygame.image.save(game_window, "output/screenshot" + str(count) + ".jpg")
        # count += 1
        universe = get_next_generation(universe=universe)
        generation_clock.tick(refresh_rate)


if __name__ == '__main__':
    error_checking()
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 800

    block_size = 10
    generation_clock = pygame.time.Clock()
    refresh_rate = 20

    # The zone where the cells live will be squared
    n_cells_x = int(min(WINDOW_WIDTH, WINDOW_HEIGHT) / block_size)
    n_cells_y = n_cells_x

    main()








