from map_generate import MapGenerator
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

N_DIRECTIONS = {SOUTH: (1, 0, NORTH),
                NORTH: (-1, 0, SOUTH),
                EAST:  (0, 1, WEST),
                WEST:  (0, -1, EAST)}

class MazeGenerator():


    def __init__(self, height, width):
        self.map = MapGenerator(height, width)

    def _valid_coordinations(self, x, y, direction):
        exist =  0 <= x < self.map.height and 0 <= y < self.map.width
        close_wall = self.map.grid[x][y] & direction
        return exist and close_wall

    def _open_wall(self, position, direction):
        x, y = position
        n_x, n_y, n_direction = N_DIRECTIONS[direction]
        n_x = x + n_x
        n_y = y + n_y
        if self.map.grid[x][y] & direction:
            self.map.grid[x][y] -= direction
        if self._valid_coordinations(n_x, n_y, direction):
            self.map.grid[n_x][n_y] -= n_direction

    def __printgrid(self):
        for row in self.map.grid:
            line = " "
            for cell in row:
                if cell == 15:
                    line += "#  "   # all walls closed
                elif cell == 0:
                    line += "   "   # all walls open
                else:
                    line += f"{cell} " # partial walls
            print(line)

    def _prin_visit(self):
        for line in self.map.visited:
            for element in line:
                if element == True:
                    print("True  ", end="")
                else:
                    print(f"{element} ", end="")
            print()

    def _get_neighbours(self,position):
        x, y = position
        validate_neighbours = []
        for validate in N_DIRECTIONS:
            n_x, n_y, direction = N_DIRECTIONS[validate]
            n_x = x + n_x
            n_y = y + n_y
            if self._is_visited((n_x, n_y)):
                validate_neighbours.append((n_x, n_y))

    def _is_visited(self, positions):
        try:
            if x < 0 or y < 0:
                return True
            x, y = positions
            return not self.map.visited[x][y]
        except IndexError:
            return True


maze = MazeGenerator(5, 7)
 
maze._prin_visit()
