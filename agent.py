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
        self.pos = []
        seedValue = random.randrange(sys.maxsize)
        random.seed(seedValue)
        self.path = []
        self.walkedSteps = 0
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
        self.pos = [i, j]
        self.walkedSteps += 1

        return [i, j]

    def walkSteps(self, grid, neigh):

        # pos = pos
        i = self.pos[0]
        j = self.pos[1]
        if neigh == 'moore':
            coordinates = [[i-1, j], [i-1, j+1], [i, j+1], [i+1, j+1], [i+1, j], [i+1, j-1], [i, j-1], [i-1, j-1]]

            for step in range(0, self.steps):
                walk = random.choice(coordinates)
                while ((walk[0] < 0 or walk[1] < 0) or (walk[0] >= len(grid) or walk[1] >= len(grid[0])) or (grid[walk[0]][walk[1]].flag != 0) ):
                    walk = random.choice(coordinates)
                i = walk[0]
                j = walk[1]
                self.walkedSteps += 1

        self.pos = walk


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
        start = (pos[0], pos[1])
        came, cost = astar.a_star_search(gridFind, start, end)
        path = astar.reconstruct_path(came, start, end)
        self.path = path
        # print(path)
        # astar.draw_grid(gridFind, width=2, path=astar.reconstruct_path(came, start=start, goal=end))
        return path

    def redCellInt(self, grid, total_facilities, scope):

        '''definição da celula ideal, deve procurar não só celulas com mais
        facilities, assim como também celulas com uma certa concentração de agentes
        parecidos, do mesmo grupo que o agente x.
        Isso deveria ser controlado por variavel estocastica dentro de um range aceitavel
        ideia aqui é atingir o grupo economico 0 e 1
        Tambem deve haver uma visão geral do mapa e das distribuições para ajudar na
        definição da "quadrante" onde esta celula ideal deve estar

        '''

        # ideia aqui, pode mesclar os vetores (linhas para areas que estão longe não serem bem conhecidas)
        al_0, newGrid = self.agentVision(grid, scope)
        center = []
        for i in range(0, len(newGrid)):
            for j in range(0, len(newGrid[0])):
                if newGrid[i][j] <= self.economicGroup:
                    center.append([i, j])

        random.shuffle(center)
        while(self.ideal == []):
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




    #
    # '''a ideia é criar uma função que vai englobar a visao do agente:
    # 1. senso de vizinhança
    #     1.1 -> densidade
    #     1.2 -> senso de vizinhança, grupo economico dos vizinhos
    #     1.3 -> atividades disponiveis (no futuro, facilities)
    #     1.4 -> Uso da Terra ao redor
    #     1.5 -> distancia de onde quer morar de fato
    #     1.6 -> Tempo da area (visão do ambiente sendo degradado pelos habitantes)
    # 2. grupo economico da celula
    # 3. dar sensação de tempo, se é o primeiro passo, agente sabe de menos coisas
    #     3.1 usar alguma variavel estocastica para realizar o "hiding" das info
    # 4. variavel de pertubação aleatoria
    # 5. Informações sobre outros agentes que estão desalocados e procurando
    # moradia ao redor de um raio do agente em questão
    #
    # R = Isso deverá fazer com que o agente pense em ocupar uma celula a qual pode não
    # estar tão perto da ideal, porem no caminho da mesma (para quando n tiver chego nela)
    # Após chegar, será usado apenas para ver se ocupa ou não, pode ter uma variavel que
    # "sabe" se chegou na celula ideal
    # '''


        # '''
        # density:        min = 0, max = 8                depends on the agent economicGroup
        # ecoGroupCell:   most frequent (or weights)      value increase with the high value of eco cell
        # ecoGroupAg:     most frequent                   value increase with the same economicGroup of agent x
        # facN:           mean of facilities in neigh     higher the better
        # newCeg:         most frequent (#2 with mask)    higher the better
        # distToRedCell:  distant to cell X               lower the better
        # timeOfSim:      the area attractiveness decay*  lower the better
        # alpha:          has the objective of control    ---
        #
        #
        # * if cell were occupied enough time
        # '''







#########
