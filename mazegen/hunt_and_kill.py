from .map import MapGenerator
import random

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

class HuntAndKill():
    def __init__(self, grid_hex, grid_flags, grid_dec, start, end, height, width, seed=15):
        self.grid_hex = grid_hex
        self.grid_flags = grid_flags
        self.grid_dec = grid_dec
        self.start = start
        self.end = end
        self.height = height
        self.width = width
        self.rrs = random.Random(seed)
        self._generate()

    def _generate(self):
        x_s, y_s = self.start

        current_x = 0
        current_y = 0

        self.grid_flags[current_x][current_y] = 2
        while True:
            neightbour = self._unvisited_neighbour((current_x, current_y))
            if neightbour:
                next_x, next_y, wall_c, wall_n = self._random_neighbour(neightbour)
                self._carve((current_x, current_y), (next_x, next_y),
                            wall_n, wall_c)
                current_x = next_x
                current_y = next_y
                self.grid_flags[current_x][current_y] = 2
            else:
                is_visited = None
                for x in range(len(self.grid_flags)):
                    for y in range(len(self.grid_flags[x])):
                        if self.grid_flags[x][y] == 0:
                            neightbour = self._visited_neighbour((x, y))
                            if neightbour:
                                next_x, next_y, wall_c, wall_n = self._random_neighbour(neightbour)
                                self._carve((next_x, next_y), (x, y),
                                            wall_n, wall_c)
                                current_x = x
                                current_y = y
                                is_visited = 1
                                break
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




    def _unvisited_neighbour(self, cell):
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

    def _visited_neighbour(self, cell):
        x, y = cell
        valid = []
        if x > 0 and self.grid_flags[x - 1][y] == 2:
            valid.append((x-1,y,NORTH, SOUTH))
        if y > 0 and self.grid_flags[x][y-1] == 2:
            valid.append((x,y-1,WEST, EAST))
        if x < self.height - 1 and self.grid_flags[x+1][y] == 2:
            valid.append((x+1,y,SOUTH, NORTH))
        if y < self.width - 1 and self.grid_flags[x][y+1] == 2:
            valid.append((x,y+1,EAST, WEST))
        return valid

    def _random_neighbour(self, neighbours):
        pick = self.rrs.choice(neighbours)
        return pick

    def _carve(self, cell, neightbour, cell_wall, neighbour_wall):
        x_c, y_c = cell
        x_n, y_n = neightbour

        self.grid_dec[x_c][y_c] -= cell_wall
        self.grid_dec[x_n][y_n] -= neighbour_wall
        self.grid_flags[x_n][y_n] = 2

    def print_maze_walls(self):
            print("+" + "---+" * self.width)
            for x in range(self.height):
                row_str = "|"
                bottom_str = "+"
                for y in range(self.width):
                    val = self.grid_dec[x][y]
                    # Eastern wall check
                    row_str += "   |" if (val & EAST) else "    "
                    # Southern wall check
                    bottom_str += "---+" if (val & SOUTH) else "   +"
                print(row_str)
                print(bottom_str)