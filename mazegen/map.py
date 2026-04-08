from .shapes import Shapes
from .hex_bin import bin_to_decimal, decimal_to_hexa
# cells not needed proparly


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


class MapGenerator():
    def __init__(self, height, width, msg=9):
        self.height = height
        self.width = width
        self.msg = msg
        # self.map = self._generate_map(height, width)
        self.flags = self._generate_flags(height, width)
        self._generate_msg()
        self.dec = bin_to_decimal(self.flags)
        self.hex = decimal_to_hexa(self.dec)


    # def _generate_map(self, height, width):
    #     grid = []
    #     for i in range(height):
    #         row = []
    #         for j in range(width):
    #             cell = CellGenerator(i, j, height, width)
    #             row.append(cell)
    #         grid.append(row)
    #     return grid


    def _generate_flags(self, height, width):
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
                self.flags[start_row + i][start_col + j] = int(msg[i][j])

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

    def load_output(self, f):
        for i in range(len(self.hex)):
            for j in range(len(self.hex[i])):
                print(self.hex[i][j], file=f, end="")
            print("", file=f)

    #just function for check will be deleted later
    def print_map(self):
            grid = self.flags
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] == 1:
                        print("#" * 2, end="")
                    else:
                        print(" " * 2, end="")
                    # print(f"{grid[i][j]} ", end="")
                print()

    def print_d(self):
        grid = self.dec
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] <= 9:
                    print(f"{grid[i][j]}  ", end="")
                else:
                    print(f"{grid[i][j]} ", end="")

            print()

    def print_h(self):
        grid = self.flags
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                print(f"{grid[i][j]} ", end="")
            print()

    def print_maze_walls(self):
        NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
        
        # 1. TOP BOUNDARY
        # We look at the top row (x=0) and draw a wall if NORTH is closed (0)
        top_line = "+"
        for y in range(self.width):
            if not (self.dec[0][y] & NORTH):
                top_line += "---+"
            else:
                top_line += "   +"
        print(top_line)
        
        for x in range(self.height):
            # 2. LEFT BOUNDARY
            # Start each row by checking if the first cell's WEST is closed
            row_str = "|" if (self.dec[x][0] & WEST) else " "
            bottom_str = "+"
            
            for y in range(self.width):
                val = self.dec[x][y]

                # Space inside the cell
                row_str += "   " 

                # 3. EAST WALLS (Right side of each cell)
                if (val & EAST):
                    row_str += "|"
                else:
                    row_str += " "
                
                # 4. SOUTH WALLS (Bottom of each cell)
                if (val & SOUTH):
                    bottom_str += "---+"
                else:
                    bottom_str += "   +"
                    
            print(row_str)
            print(bottom_str)


    def print_maze_from_flags(self):
        grid = self.flags
        rows = self.height
        cols = self.width

        # 1. Draw the top boundary
        top = "+"
        for y in range(cols):
            # Only open the ceiling if the cell is 1 (optional, usually top is closed)
            top += "---+"
        print(top)

        for x in range(rows):
            # 2. Start row with a wall
            row_str = "|"
            bottom_str = "+"

            for y in range(cols):
                # Check East: If current is 1 AND neighbor to the right is 1, open it
                if y < cols - 1 and grid[x][y] == 1 and grid[x][y+1] == 1:
                    row_str += "    " # Space + no wall
                else:
                    row_str += "   |" # Space + wall

                # Check South: If current is 1 AND neighbor below is 1, open it
                if x < rows - 1 and grid[x][y] == 1 and grid[x+1][y] == 1:
                    bottom_str += "   +" # No wall + joint
                else:
                    bottom_str += "---+" # Wall + joint

            print(row_str)
            print(bottom_str)

# test = MapGenerator(11, 15)
# test.print_h(decimal_to_hexa(test.map))
# test.print_map()
