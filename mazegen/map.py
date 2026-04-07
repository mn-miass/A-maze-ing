from cells import CellGenerator
from shapes import Shapes

class MapGenerator():
    def __init__(self, height, width, msg=99):
        self.height = height
        self.width = width
        self.msg = msg
        self.map = self._generate_map(height, width)
        self.bin = self._generate_bin(height, width)
        self._generate_msg()

    def _generate_map(self, height, width):
        grid = []
        for i in range(height):
            row = []
            for j in range(width):
                cell = CellGenerator(i, j, height, width)
                row.append(cell)
            grid.append(row)
        return grid

    def _generate_bin(self, height, width):
        grid = []
        for i in range(height):
            row = []
            for j in range(width):
                cell = 0
                row.append(cell)
            grid.append(row)
        return grid

    def _generate_msg(self):
        msg = self._get_number()
        start_row = (self.height - len(msg)) // 2
        start_col = (self.width - len(msg[0])) // 2
        for i in range(len(msg)):
            for j in range(len(msg[0])):
                self.bin[start_row + i][start_col + j] = int(msg[i][j])

    def _get_number(self):
        tens = self.msg // 10
        tens_grid = []
        ones = self.msg % 10
        ones_grid = []

        if tens == 0:
            tens_grid = Shapes._shape_0()
        elif tens == 1:
            tens_grid = Shapes._shape_1()
        elif tens == 2:
            tens_grid = Shapes._shape_2()
        elif tens == 3:
            tens_grid = Shapes._shape_3()
        elif tens == 4:
            tens_grid = Shapes._shape_4()
        elif tens == 5:
            tens_grid = Shapes._shape_5()
        elif tens == 6:
            tens_grid = Shapes._shape_6()
        elif tens == 7:
            tens_grid = Shapes._shape_7()
        elif tens == 8:
            tens_grid = Shapes._shape_8()
        elif tens == 9:
            tens_grid = Shapes._shape_9()

        if ones == 0:
            ones_grid = Shapes._shape_0()
        elif ones == 1:
            ones_grid = Shapes._shape_1()
        elif ones == 2:
            ones_grid = Shapes._shape_2()
        elif ones == 3:
            ones_grid = Shapes._shape_3()
        elif ones == 4:
            ones_grid = Shapes._shape_4()
        elif ones == 5:
            ones_grid = Shapes._shape_5()
        elif ones == 6:
            ones_grid = Shapes._shape_6()
        elif ones == 7:
            ones_grid = Shapes._shape_7()
        elif ones == 8:
            ones_grid = Shapes._shape_8()
        elif ones == 9:
            ones_grid = Shapes._shape_9()
        num = self.add_blocks(tens_grid, ones_grid)
        return num

    def add_blocks(self, block_a, block_b):
        added_block = []
        for i in range(len(block_a)):
            row_block = []
            for j in range(len(block_a[i])):
                row_block.append(block_a[i][j])
            row_block.append(False)
            for j in range(len(block_b[i])):
                row_block.append(block_b[i][j])
            added_block.append(row_block)
        return added_block

    def print_map(self):
            grid = self.bin
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] == 1:
                        print("#" * 2, end="")
                    else:
                        print(" " * 2, end="")
                    # print(f"{grid[i][j]} ", end="")
                print()


test = MapGenerator(30, 50)
test.print_map()
