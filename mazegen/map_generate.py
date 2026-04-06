class MapGenerator():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self._generate_grid()
        self.visited = self._generate_visit()

    def _generate_grid(self):
        grid = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(15)
            grid.append(row)
        return grid

    def _generate_visit(self):
        visited = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            visited.append(row)
        return visited
