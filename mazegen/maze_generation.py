from .hundle_input import HundleInput
from .hunt_and_kill import HuntAndKill
from .hex_bin import hexa_to_bin, bin_to_decimal, decimal_to_hexa
from .shapes import Shapes
from .map import MapGenerator


class MazeGenerator():
    def __init__(self, data):
        self.data = data
        self.hex_map = []
        self.flags_map = []
        self.dec_map = []
        self._generate()

    def _generate(self):
        self.data = HundleInput(self.data)
        if self.data == False:
            exit(0)
        print(self.data.data_list)
        map = MapGenerator(self.data.height, self.data.width, self.data.msg)
        print(self.data.msg)
        self.hex_map = map.hex
        self.flags_map = map.flags
        self.dec_map = map.dec
        map.print_maze_from_flags()
        # maze = HuntAndKill(self)


test_data = {
    "width": "20",
    "HEIGHT": 15,
    "entry": "0,1",
    "EXIT": "19,14",
    "output_file": "maze_result.txt",
    "PERFECT": "true",
    "seed": "1337",
    "msg": 10
}
maze = MazeGenerator(test_data)