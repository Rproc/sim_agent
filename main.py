from cell import Cell
from model import Model
import numpy as np
from agent import Agent
import random
import sys
from statistics import mean, median
seedValue = random.randrange(sys.maxsize)
random.seed(seedValue)


consolidationTime = 5
decay = 8
density = 0.66
alpha = 0.95
threshold = 0.5
size = [8, 8]
age = list(np.zeros(size[0]*size[1], dtype=np.int))
flag = list(np.zeros(size[0]*size[1], dtype=np.int))
# flag = [0, 0, 0, 0, 1, 0, 0, 1, 0]
# x = [0, 0, 0, 1, 1, 1, 2, 2, 2]
# y = [0, 1, 2, 0, 1, 2, 0, 1, 2]
# cellEcoGroup = [0, 0, 0, 0, 0, 0, 0, 0, 0]
# steps = [2, 2, 2, 2, 2, 2, 2, 2, 2]

eco = [0, 1, 2]
fac = [[0, 1, 2], [0, 1], [0]]
x = []
y = []
cellEcoGroup = []
steps = []
facilities = []
for i in range(0, size[0]):
    for j in range(0, size[1]):
        x.append(i)
        y.append(j)
        cellEcoGroup.append(random.choices(eco, weights=(60, 30, 10), k=1)[0])
        facilities.append(random.choices(fac)[0])
        steps.append(2)

neigh = 'moore'
# print(cellEcoGroup)
test = Model(size[0]*size[1], [0.6, 0.3, 0.12], consolidationTime, decay, density, [], alpha, threshold, facilities=facilities, total_facilities=len(fac))
test.mapGrid(size, x, y, flag, cellEcoGroup, age, facilities)


l = test.createAgents(steps)
# print(l[0].path)
# d, i = test.eval(neigh, l[0].ideal, l[0], 1, 0.5, 2, len(l[0].path)-1)
hist = test.simulation(neigh,1, steps)

print('max: ', max(hist))
con = 0
f = open('out.txt', 'w')
for elem in hist:
    if elem > 0.25:
        con+= 1
    f.write(str(elem) + '\n')

print('elemns > 0.25: ', con, 'of: ', len(hist))
print('mean: ', mean(hist),'median: ', median(hist))
f.close()
# a = 0
# for ag in l:
#     print('ag allocated: ', ag.allocated)
#     a += 1
#
# if a == len(l):
#     print('all allocated')
# for ag in l:
#     print(ag.ideal)
# l[0].redCellInt(test.grid, 1, 3)
# vis, g = l[0].agentVision(test.grid, 2)
# print('vis:', vis)
# print(g)

# test.simulation(neigh, 1, steps)



















################# End ############################
