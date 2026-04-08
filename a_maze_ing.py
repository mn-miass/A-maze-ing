import sys
import mazegen
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
    #check if there is somthing missing

    #print to the output file the map as hex
    map = mazegen.MapGenerator(data["HEIGHT"], data["WIDTH"])
    map.print_map()
    with open(data["OUTPUT_FILE"], "w") as file:
        map.load_output(file)
    map = mazegen.MazeGenerator(map.hex, map.flags, map.dec, data["ENTRY"], data["EXIT"], map.height, map.width)
    map.print_maze_walls()
    
