from cell import Cell
from agent import Agent
import math
import random
import sys
class Model:


    def __init__(self, numberAgents, divisionAgents, consolidationTime, decayStartPoint, density, grid):

        self.numberAgents = numberAgents
        self.divisionAgents = divisionAgents
        self.consolidationTime = consolidationTime
        self.decayStartPoint = decayStartPoint
        self.density = density
        self.grid = grid

    def mapGrid(self, size, x, y, flag, cellEcoGroup, age, agent=None):
        # print(size)

        self.grid = []
        width = size[0]
        height = size[1]
        for i in range(0, width):
            g = []
            for j in range(0, height):
                c = Cell(x[i*width+j], y[i*width+j], flag[i*width+j], cellEcoGroup[i*width+j], age[i*width+j], agent)
                g.append(c)

            self.grid.append(g)

    def periferization(self, neigh, i, j):

        # for i in range(0, len(self.grid)):
        #     for j in range(0, len(self.grid[0])):
        #         self.grid[i][j].age += 1
        #         # print (grid[i][j].age)
        if self.grid[i][j].age >= self.consolidationTime and self.grid[i][j].cellEcoGroup == 0:
            self.grid[i][j].consolidate = True

        if self.grid[i][j].age >= self.decayStartPoint and self.grid[i][j].cellEcoGroup == 2:
            d = neighborhood(neigh, i, j, len(self.grid[0]))
            # if greater, abandon cell
            if d >= density:
                self.grid[i][j].agent.allocated = False
                self.grid[i][j].agent = None

    def neighborhood(self, neigh, i, j, row):

        if neigh == 'moore':

            coordinates = [[i-1, j], [i-1, j+1], [i, j+1], [i+1, j+1], [i+1, j], [i+1, j-1], [i, j-1], [i-1, j-1]]

            near = 0

            for (x, y) in coordinates:
                if (x < 0 or y < 0) or (x > len(self.grid) or y > len(self.grid[0])):
                    pass
                else:
                    if self.grid[x][y].agent != None:
                        near+=1

        return near

    # def agentWalk(self):

    def createAgents(self):

        groupZero = math.floor(self.numberAgents * self.divisionAgents[0]) # Low Economics
        groupOne = math.floor(self.numberAgents * self.divisionAgents[1]) # Mid Economics
        groupTwo = math.floor(self.numberAgents * self.divisionAgents[2]) # High Economics

        ag = [groupZero, groupOne, groupTwo]
        listAgents = []

        for elem in ag:
            for i in range(0, elem):
                a = Agent(i, False)
                listAgents.append(a)

        return listAgents


    # def allocateAgents(self, agents):
    #
    #     seedValue = random.randrange(sys.maxsize)
    #     random.seed(seedValue)
    #     maxX = len(self.grid)
    #     maxY = len(self.grid[0])
    #     sequenceX = [i for i in range(maxX)]
    #     sequenceY = [i for i in range(maxY)]
    #     for agent in agents:
    #         i = random.choice(sequenceX)
    #         j = random.choice(sequenceY)
    #
    #         while (self.grid[i][j].flag == 1 or self.grid[i][j].cellEcoGroup > agent.economicGroup):
    #             i = random.choice(sequenceX)
    #             j = random.choice(sequenceY)
    #
    #         agent.allocated = True
    #         self.grid[i][j].agent = agent


    def simulation(self, neigh, timeOfSim):

        for t in range(0, timeOfSim):
            for i in range(0, len(self.grid)):
                for j in range(0, len(self.grid[0])):

                    l = self.createAgents()

                    self.allocateAgents(l)

                    #first do things with cells
                    self.periferization(neigh, i, j)

                    # self.randomWalk(self)












##
