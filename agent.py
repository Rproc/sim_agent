import numpy as np
import os
import random
import sys
class Agent:

    def __init__(self, economicGroup, allocated, steps, ideal=[]):
        self.economicGroup = economicGroup
        self.allocated = False
        self.steps = steps
        self.ideal = ideal
        # self.density = density


    def redCell(self, grid):

        center = [(ind, grid[ind].index(0)) for ind in range(len(grid)) if 0 in grid[ind]]
        for i in range(0, len(grid)):
            for j in range(0, len(grid[0])):
                if grid[i][j].cellEcoGroup >= 0:
                    center.append([i, j])
        # print(center)

        seedValue = random.randrange(sys.maxsize)
        random.seed(seedValue)
        goal = random.choice(center)

        self.ideal = list(goal)

    def randomWalk(self, grid):
        maxX = len(grid)
        maxY = len(grid[0])
        sequenceX = [i for i in range(maxX)]
        sequenceY = [i for i in range(maxY)]

        i = random.choice(sequenceX)
        j = random.choice(sequenceY)

        return [i, j]

    def walkSteps(self, grid, neigh):

        pos = self.ideal
        i = pos[0]
        j = pos[1]
        if neigh == 'moore':
            coordinates = [[i-1, j], [i-1, j+1], [i, j+1], [i+1, j+1], [i+1, j], [i+1, j-1], [i, j-1], [i-1, j-1]]

            for step in range(0, self.steps):
                walk = random.choice(coordinates)
                while ((walk[0] < 0 or walk[1] < 0) or (walk[0] >= len(grid) or walk[1] >= len(grid[0])) or (grid[walk[0]][walk[1]].flag != 0) ):
                    walk = random.choice(coordinates)
                i = walk[0]
                j = walk[1]

        return walk
