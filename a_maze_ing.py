import sys
import parse
import mazegen

if __name__ == "__main__":
    if len(sys.argv) == 1:
        #print no argument was given
        exit(1)

    if sys.argv[1] != "config.txt":
        #print the wrong file was given
        pass

    data = parse.parsing(sys.argv[1])
    maze = mazegen.MazeGenerator(data)
    with open(data["OUTPUT_FILE"], "w") as file:
        for x in range(maze.data.height):
            for y in range(maze.data.width):
                file.write(str(maze.hex_map[x][y]))
            print("", file=file)
    #check if there is somthing missing

    # print to the output file the map as hex
    # map = mazegen.MapGenerator(10, 10, 42)
    # map.print_maze_walls()
    # map.print_maze_from_flags()
    # map.print_maze_walls()

