from .map import MapGenerator

class MazeGenerator():
    def __init__(self, grid_hex, grid_bit, start, end):
        self.grid_hex = grid_hex
        self.grid_bit = grid_bit
        self.start = start
        self.end = end

    def _generate(self):
        ...

    def _valid_neighbour(self):
        pass

    def _random_neighbour(self):
        pass

    def _carve(self, row, col, next_row, next_col):
        pass