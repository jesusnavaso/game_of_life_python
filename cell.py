class Cell:
    """ Simple class for representing a cell.
    When the status is True the cell is alive and if it is false, the cell is dead"""

    status = True
    x_pos = 0
    y_pos = 0

    def __init__(self, status: bool, x_pos: int, y_pos: int):
        self.status = status
        self.x_pos = x_pos
        self.y_pos = y_pos

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        else:
            return self.x_pos == other.x_pos and self.y_pos == other.y_pos

    def __str__(self):
        cell_status = "Alive" if self.status else "Dead"
        return f"({self.x_pos},{self.y_pos}): {cell_status}"

