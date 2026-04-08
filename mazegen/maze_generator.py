from .map import MapGenerator
import random

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

class MazeGenerator():
    def __init__(self, grid_hex, grid_flags, grid_dec, start, end, height, width, seed=42):
        self.grid_hex = grid_hex
        self.grid_flags = grid_flags
        self.grid_dec = grid_dec
        self.start = start
        self.end = end
        self.height = height
        self.width = width
        self.rrs = random.Random(seed)

    def _generate(self):
        x_s, y_s = self.start
        # self.grid_flags[x_s][y_s] = "Start"
        # self.grid_flags[x_e][y_e] = "End"

        current_x = x_s
        current_y = y_s

        is_visited = self.grid_flags[current_x][current_y]
        while is_visited == 0:
            neightbour = self._valid_neighbour((current_x, current_y))
            if neightbour != []:
                pick = self._random_neighbour(neightbour)
                self._carve((current_x, current_y), (pick[0], pick[1]),
                            pick[3], pick[4])
                current_x = pick[0]
                current_y = pick[1]
                self.grid_flags[current_x][current_y] = 1
                is_visited = self.grid_flags[current_x][current_y]
            else:
                is_visited = None
                for x in range(len(self.grid_flags)):
                    for y in range(len(self.grid_flags[x])):
                        if self.grid_flags[x][y] == 1:
                            neightbour = self._valid_neighbour((x, y))
                            pick = self._random_neighbour(neightbour)
                            if pick != ():
                                pick = self._random_neighbour(neightbour)
                                self._carve((current_x, current_y), (pick[0], pick[1]),
                                            pick[3], pick[4])
                                current_x = pick[0]
                                current_y = pick[1]
                                is_visited = 0
            if is_visited == None:
                break
     
        #is_visited will hold coordination
        #while is_visited
        #   check for valid neighbour 
        #       pick one randomly 
        #   if there is no one 
        #       loop until you found a valid one from x = 0, y = 0 y++ x++
        #           if there is none set is_visited to false
        #           break the loop if validate rest None and return none
        #break if is validate is none




    def _valid_neighbour(self, cell):
        x, y = cell
        valid = []
        if x > 0 and self.grid_flags[x - 1][y] == 0:
            valid.append((x-1,y,NORTH, SOUTH))
        if y > 0 and self.grid_flags[x][y-1] == 0:
            valid.append((x,y-1,EAST, WEST))
        if x < self.height - 1 and self.grid_flags[x+1][y] == 0:
            valid.append((x+1,y,SOUTH, NORTH))
        if y < self.width - 1 and self.grid_flags[x][y+1] == 0:
            valid.append((x,y+1,WEST, EAST))
        return valid


    def _random_neighbour(self, neighbours):
        pick = self.rrs.choice(neighbours)
        return pick

    def _carve(self, cell, neightbour, cell_wall, neighbour_wall):
        x_c, y_c = cell
        x_n, y_n = neightbour

        self.grid_hex[x_c][y_c] -= cell_wall
        self.grid_hex[x_n][y_n] -= neighbour_wall
        self.grid_flags[x_n][y_n] = 1

    def print_map(self):
            grid = self.grid_
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] == 1:
                        print("#" * 2, end="")
                    else:
                        print(" " * 2, end="")
                    # print(f"{grid[i][j]} ", end="")
                print()