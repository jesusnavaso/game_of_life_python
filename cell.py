class Cell:
    """ Simple class for representing a cell
    when the status is True the cell is alive and if it is false, the cell is dead"""

    status = True
    # n_neighbours = 0
    x_pos = 0
    y_pos = 0

    def __init__(self, status: bool, x_pos: int, y_pos: int):
        self.status = status
        self.x_pos = x_pos
        self.y_pos = y_pos

    # def __init__(self, status: bool, x_pos: int, y_pos: int, n_neighbours: int = 0):
    #     self.status = status
    #     self.x_pos = x_pos
    #     self.y_pos = y_pos
    #     self.n_neighbours = n_neighbours