import numpy as np
import os
import random
import sys
import astar
from scipy import stats as s
import monteCarlo as mc
class Agent:

    def __init__(self, economicGroup, allocated, steps, ideal=[]):
        self.economicGroup = economicGroup
        self.allocated = False
        self.steps = steps
        self.ideal = ideal
        seedValue = random.randrange(sys.maxsize)
        random.seed(seedValue)
        # self.density = density

    def redCell(self, grid):

        center = [(ind, grid[ind].index(0)) for ind in range(len(grid)) if 0 in grid[ind]]
        for i in range(0, len(grid)):
            for j in range(0, len(grid[0])):
                if grid[i][j].cellEcoGroup >= 0:
                    center.append([i, j])
        # print(center)


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

    def walkToRedCell(self, grid, pos):

        gridFind = astar.GridWithWeights(len(grid), len(grid[0]))
        new = []
        for i in range(0, len(grid)):
            for j in range(0, len(grid[0])):
                if grid[i][j].flag == 1:
                    new.append((i, j))

        gridFind.weights = {loc: 5 for loc in new}
        gridFind.walls = new
        end = (self.ideal[0], self.ideal[1])
        start = (pos[0], pos(1))
        came, cost = astar.a_star_search(gridFind, start, end)
        path = astar.reconstruct_path(came, start, end)
        print(path)
        astar.draw_grid(gridFind, width=2, path=astar.reconstruct_path(came, start=start, goal=end))
        return path

    def redCellInt(self, grid, simTime, total_facilities):

        '''definição da celula ideal, deve procurar não só celulas com mais
        facilities, assim como também celulas com uma certa concentração de agentes
        parecidos, do mesmo grupo que o agente x.
        Isso deveria ser controlado por variavel estocastica dentro de um range aceitavel
        ideia aqui é atingir o grupo economico 0 e 1
        Tambem deve haver uma visão geral do mapa e das distribuições para ajudar na
        definição da "quadrante" onde esta celula ideal deve estar

        '''
        if simTime < 2:
            scope = 2
        if simTime >= 2 and simTime < 4:
            scope = 4
        else:
            scope = len(grid)
        # ideia aqui, pode mesclar os vetores (linhas para areas que estão longe não serem bem conhecidas)
        a, newGrid = self.agentVision(grid, scope)
        center = []
        for i in range(0, len(newGrid)):
            for j in range(0, len(newGrid[0])):
                if newGrid[i][j] <= self.economicGroup:
                    center.append([i, j])

        random.shuffle(center)
        for elem in center:
            cellFac = len(grid[elem[0]][elem[1]].facilities)/total_facilities
            if cellFac >= mc.crude_monte_carlo():
                self.ideal = elem
                break

    def agentVision(self, grid, scope):
        x = int(len(grid)/scope)
        y = int(len(grid[0])/scope)
        g = []
        gridVision = []
        a = []

        for i in range(0, len(grid), x):
            aux = []
            for j in range(0, len(grid[0]), y):
                l = []
                for w in range(i, i+x):
                    for h in range(j, j+y):
                        l.append(grid[w][h].cellEcoGroup)
                aux.append(int(s.mode(l)[0]))
                for el in range(0, len(l)):
                    a.append(int(s.mode(l)[0]))

            gridVision.append(aux)

        for i in range(0, len(grid)):
            aux = []
            for j in range(0, len(grid[0])):
                aux.append(a[i*len(grid)+j])
            g.append(aux)

        return gridVision, g

















#########
