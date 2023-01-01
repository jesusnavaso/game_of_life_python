class Cell:
    """ Simple class for representing a cell."""

    def __init__(self, alive: bool, x_pos: int, y_pos: int):
        self.alive = alive
        self.x_pos = x_pos
        self.y_pos = y_pos

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        else:
            return self.x_pos == other.x_pos and self.y_pos == other.y_pos

    def __str__(self):
        cell_status = "Alive" if self.alive else "Dead"
        return f"({self.x_pos},{self.y_pos}): {cell_status}"

    def __hash__(self):
        return self.x_pos * 10000 + self.y_pos
