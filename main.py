from cell import Cell
from model import Model
import numpy as np
from agent import Agent
import pprint
# economicGroup, agent settled, number in space (x,y)

consolidationTime = 5
decay = 8
density = 9
size = [3, 3]
age = list(np.zeros(9, dtype=np.int))
flag = list(np.zeros(9, dtype=np.int))
x = [0, 0, 0, 1, 1, 1, 2, 2, 2]
y = [0, 1, 2, 0, 1, 2, 0, 1, 2]
cellEcoGroup = [0, 0, 0, 0, 0, 0, 0, 0, 0]
neigh = 'moore'
    # def __init__(self, numberAgents, divisionAgents, consolidationTime, decayStartPoint, density, grid):
steps = [2, 2, 2, 2, 2, 2, 2, 2, 2]

test = Model(9, [0.7, 0.3, 0.2], consolidationTime, decay, density, [])
test.mapGrid(size, x, y, flag, cellEcoGroup, age)
# print(test.grid[0][1])

test.simulation('moore', 5, steps)
# for i in range(0, 3):
#     for j in range(0, 3):
#         print(test.neighborhood(neigh, i, j, 3))#         print(i, j)
a = []
for i in range(0, len(test.grid)):
    for j in range(0, len(test.grid[0])):
        a.append(test.grid[i][j].cellEcoGroup)


for i in range(0, 3):
    for j in range(0, 3):
        print(a[i*3+j], end='\t')
    print()
# l = test.createAgents(steps)

# test.allocateAgents(l)
# for el in l
#
# for ag in l:
#     print(ag.economicGroup, ag.ideal, ag.allocated)

# print(l, len(l), l[0].economicGroup, l[2].economicGroup, l[6].economicGroup)
# print(test.grid[0][0].cellEcoGroup)
# print(grid[0][0].consolidate)
# print(grid[2][2].cellEcoGroup)
#
# for t in range(0, 6):
#     for i in range(0, len(grid)):
#         for j in range(0, len(grid[0])):
#             grid[i][j].age += 1
#             # print (grid[i][j].age)
#             if grid[i][j].age >= consolidationTime and grid[i][j].cellEcoGroup == 0:
#                 grid[i][j].consolidate = True
#
#
# for i in range(0, len(grid)):
#     for j in range(0, len(grid[0])):
#         print(i, j, "eco group:", grid[i][j].cellEcoGroup, "consolidated: ", grid[i][j].consolidate)


# agent = Agent(1)
# c = Cell(1, 1, 0, 1, 1, agent=agent)
# print(c.agent)
# print(c.agent.economicGroup)
