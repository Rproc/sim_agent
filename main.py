from cell import Cell
from model import Model
import numpy as np
# economicGroup, agent settled, number in space (x,y)

consolidationTime = 5
decay = 8
density = 2
size = [3, 3]
age = list(np.zeros(9, dtype=np.int))
flag = list(np.zeros(9, dtype=np.int))
x = [0, 0, 0, 1, 1, 1, 2, 2, 2]
y = [0, 1, 2, 0, 1, 2, 0, 1, 2]
cellEcoGroup = [0, 0, 0, 1, 2, 1, 0, 1, 1]


test = Model(10, [0.1, 0.3, 0.6], consolidationTime, decay, density)
grid = test.mapGrid(size, x, y, flag, cellEcoGroup, age)

# print(grid[0][0].consolidate)
# print(grid[2][2].cellEcoGroup)
#
for t in range(0, 6):
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            grid[i][j].age += 1
            # print (grid[i][j].age)
            if grid[i][j].age >= consolidationTime and grid[i][j].cellEcoGroup == 0:
                grid[i][j].consolidate = True


for i in range(0, len(grid)):
    for j in range(0, len(grid[0])):
        print(i, j, "eco group:", grid[i][j].cellEcoGroup, "consolidated: ", grid[i][j].consolidate)
