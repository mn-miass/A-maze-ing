from .map import MapGenerator
import random

class MazeGenerator():
    def __init__(self, grid_hex, grid_flags, grid_dec, start, end, height, width, seed=42):
        self.grid_hex = grid_hex
        self.grid_flags = grid_flags
        self.grid_dec = grid_dec
        self.start = start
        self.end = end
        self.height = height
        self.width = width

    def _generate(self):
        x_s, y_s = self.start
        x_e, y_e = self.end
        self.grid_flags[x_s][y_s] = "Start"
        self.grid_flags[x_e][y_e] = "End"


    def _valid_neighbour(self, cell):
        x, y = cell
        valid = []
        if x > 0 and self.grid_flags[x - 1][y] == 0:
            valid.append([x-1][y])
        if y > 0 and self.grid_flags[x][y-1] == 0:
            valid.append([x][y-1])
        if x < self.height - 1 and self.grid_flags[x+1][y] == 0:
            valid.append([x+1][y])
        if y < self.width - 1 and self.grid_flags[x][y+1] == 0:
            valid.append([x][y+1])
        return valid


    def _random_neighbour(self, neighbours, seed):
        random.seed(seed)
        pick = random.choice(neighbours)
        return pick

    def _carve(self, cell, neightbour):
        pass