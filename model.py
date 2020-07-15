from cell import Cell
from agent import Agent

class Model:


    def __init__(self, numberAgents, divisionAgents, consolidationTime, decayStartPoint, density):

        self.numberAgents = numberAgents
        self.divisionAgents = divisionAgents
        self.consolidationTime = consolidationTime
        self.decayStartPoint = decayStartPoint
        self.density = density



    def mapGrid(self, size, x, y, flag, cellEcoGroup, age, agent=None):
        # print(size)

        grid = []
        width = size[0]
        height = size[1]
        for i in range(0, width):
            g = []
            for j in range(0, height):
                c = Cell(x[i*width+j], y[i*width+j], flag[i*width+j], cellEcoGroup[i*width+j], age[i*width+j], agent)
                g.append(c)
                # print(c.x, c.y, c.flag, c.cellEcoGroup, c.age)

            grid.append(g)

        return grid
