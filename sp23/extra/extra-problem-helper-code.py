def create_diamond(pattern : str) -> list:
    pattern_length = len(pattern)
    grid_size = 2 * pattern_length - 1
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)] # create n x n grid

    for i in range(pattern_length): # looping over the alphabet
        for j in range(pattern_length - i): # looping over the grid
            grid[pattern_length - 1 - j][i + j] = pattern[i] # top left quadrant
            grid[pattern_length - 1 + j][i + j] = pattern[i] # bottom left quadrant
            grid[pattern_length - 1 + j][grid_size - 1 - i - j] = pattern[i] # bottom right quadrant
            grid[pattern_length - 1 - j][grid_size - 1 - i - j] = pattern[i] # top right quadrant
    return grid

grid = create_diamond('GERANDY')

for row in grid:
    print(row)

GOAL = 'GERANDYDNAREG'
def traverse_grid(coord: tuple, path: str, trajectory: list = None) -> int:
    '''Recursive algorithm that counts the number of paths to spell GOAL given starting coordinate.
        If trajectory is not None, then no path can visit a coordinate twice.
    
    Parameters:
        coord: the current coordinate being visited
        path: the path that has been traversed so far
        trajectory: a list of coordinates that have been visited so far
    '''
    # check if out of bounds or if coord has been visited before
    if (coord[0] < 0 or coord[0] >= len(grid) or coord[1] < 0 or coord[1] >= len(grid[0])) \
        or (trajectory != None and coord in trajectory):
        return 0

    # add point to path
    path += grid[coord[0]][coord[1]]

    # base case
    if path == GOAL:
        return 1
    
    # check if path is a prefix of GOAL
    if path != GOAL[0:len(path)]:
        return 0
    
    # add coord to trajectory
    if trajectory != None:
        trajectory.append(coord)
    
    # recursive case
    sum = 0
    sum += traverse_grid((coord[0], coord[1] - 1), path, trajectory) # traverse left
    sum += traverse_grid((coord[0], coord[1] + 1), path, trajectory) # traverse right
    sum += traverse_grid((coord[0] - 1, coord[1]), path, trajectory) # traverse up
    sum += traverse_grid((coord[0] + 1, coord[1]), path, trajectory) # traverse down

    return sum

# Brute force method to count the number of paths from every coordinate
# WITH traversing the same coordinate twice
sum = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        sum += traverse_grid((i, j), "")
print(sum)

# Brute force method to count the number of paths from every coordinate
# WITHOUT traversing the same coordinate twice
sum = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        sum += traverse_grid((i, j), "", [])

print(sum)