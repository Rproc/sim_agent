from cell import Cell
from agent import Agent
import math
import random
import sys
from collections import deque
import queue


class Model:


    def __init__(self, numberAgents, divisionAgents, consolidationTime, decayStartPoint, density, grid, alpha, facilities=[], total_facilities=0):

        self.numberAgents = numberAgents
        self.divisionAgents = divisionAgents
        self.consolidationTime = consolidationTime
        self.decayStartPoint = decayStartPoint
        self.density = density
        self.grid = grid
        self.facilities = facilities
        self.total_facilities = total_facilities
        self.alpha = alpha

        seedValue = random.randrange(sys.maxsize)
        random.seed(seedValue)

    def mapGrid(self, size, x, y, flag, cellEcoGroup, age, facilities, agent=None):
        # print(size)

        self.grid = []
        width = size[0]
        height = size[1]
        for i in range(0, width):
            g = []
            for j in range(0, height):
                c = Cell(x[i*width+j], y[i*width+j], flag[i*width+j], cellEcoGroup[i*width+j], age[i*width+j], facilities[i*width+j], agent)
                g.append(c)

            self.grid.append(g)

    def periferization(self, neigh, i, j):

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
            ceg = []
            aeg = []
            facN = []

            for (x, y) in coordinates:
                if (x < 0 or y < 0) or (x >= len(self.grid) or y >= len(self.grid[0])):
                    pass
                else:
                    if self.grid[x][y].agent != None:
                        near+=1
                        aeg.append(self.grid[x][y].agent.economicGroup)
                    ceg.append(self.grid[x][y].cellEcoGroup)
                    facN.append(len(self.grid[x][y].facilities))

        return near, ceg, aeg, facN

    def createAgents(self, steps):

        groupZero = math.floor(self.numberAgents * self.divisionAgents[0]) # Low Economics
        groupOne = math.floor(self.numberAgents * self.divisionAgents[1]) # Mid Economics
        groupTwo = math.floor(self.numberAgents * self.divisionAgents[2]) # High Economics

        ag = [groupZero, groupOne, groupTwo]
        print(ag)
        # print (ag)
        ec = [0, 1, 2]
        listAgents = []
        j = 0
        k = 0
        for elem in ag:
            for i in range(0, elem):
                a = Agent(ec[k], False, steps[j])
                j += 1
                a.redCellInt(self.grid, self.total_facilities, 2)
                listAgents.append(a)
            k += 1
        return listAgents

    def allocateAgents(self, agents):

        maxX = len(self.grid)
        maxY = len(self.grid[0])
        sequenceX = [i for i in range(maxX)]
        sequenceY = [i for i in range(maxY)]
        for agent in agents:
            i = random.choice(sequenceX)
            j = random.choice(sequenceY)

            while (self.grid[i][j].flag == 1 or self.grid[i][j].cellEcoGroup > agent.economicGroup):
                i = random.choice(sequenceX)
                j = random.choice(sequenceY)

            agent.allocated = True
            self.grid[i][j].agent = agent

    # def randomWalk(self, agent):
    #     maxX = len(self.grid)
    #     maxY = len(self.grid[0])
    #     sequenceX = [i for i in range(maxX)]
    #     sequenceY = [i for i in range(maxY)]
    #
    #     i = random.choice(sequenceX)
    #     j = random.choice(sequenceY)
    #
    #     return [i, j]
    #
    # def walkSteps(self, ag, neigh):
    #
    #     pos = ag.ideal
    #     i = pos[0]
    #     j = pos[1]
    #     if neigh == 'moore':
    #         coordinates = [[i-1, j], [i-1, j+1], [i, j+1], [i+1, j+1], [i+1, j], [i+1, j-1], [i, j-1], [i-1, j-1]]
    #
    #         for step in range(0, ag.steps):
    #             walk = random.choice(coordinates)
    #             while ((walk[0] < 0 or walk[1] < 0) or (walk[0] > len(self.grid) or walk[1] > len(self.grid[0])) or (self.grid[walk[0]][walk[1]].flag != 0) ):
    #                 walk = random.choice(coordinates)
    #             i = walk[0]
    #             j = walk[1]
    #
    #     return walk

    def eval(self, neigh, pos, ag, timeOfSim, alpha, scope, distToRedCell):

        # mudar para o newGrid, calcular ele e mascarar Informações
        density, ecoGroupCell, ecoGroupAg, facN = self.neighborhood(neigh, local[0], local[1], len(self.grid[0]))

        # distancia da celula, quanto mais distante, tem que pesar mais
        distToRedCell

        # tempo de simulação, quanto maior, menos atrativo fica a area, se essa celula ja tiver ocupada
        timeOfSim



        # o resultado de tudo vezes ela
        alpha


        return density, indexOccup


    def evict(self, ag, x, y):
        agExpelled = self.grid[x][y].agent

        self.grid[x][y].settle(ag)

        return agExpelled

    def simulation(self, neigh, timeOfSim, steps):

        l = self.createAgents(steps)
        agQueue = queue.Queue()

        for t in range(0, timeOfSim):
            print('time: ', t)

            if t < 2:
                scope = 2
            if t >= 2 and t < 4:
                scope = 4
            else:
                scope = len(grid)

            for i in range(0, len(self.grid)):
                for j in range(0, len(self.grid[0])):

                    # self.allocateAgents(l)
                    #first do things with cells
                    if (t > 1):
                        self.periferization(neigh, i, j)

                    for elem in l:
                        agQueue.put(elem)

                    while not agQueue.empty():

                        ag = agQueue.get()

                        if t > 1 and ag.allocated == False:
                            ag.redCellInt(self.grid, self.total_facilities, scope)
                        pos = ag.randomWalk(self.grid)

                        path_to_ideal = ag.walkToRedCell(self.grid, pos)
                        # print(path_to_ideal)
                        # for coord in path_to_ideal:
                        #     x, y = coord
                        #     pos = [x, y]

                        while (ag.allocated == False):
                            if len(path_to_ideal) > 0:
                                x, y = path_to_ideal.pop(0)
                                local = [x, y]
                                ag.pos = local
                            else:
                                local = ag.walkSteps(self.grid, neigh, pos)
                            # vision, in the future, or something that will compose the vision
                            d, indexOccup = self.eval(neigh, local, ag, t, self.alpha, scope, len(path_to_ideal))
                            '''a ideia é criar uma função que vai englobar a visao do agente:
                            1. senso de vizinhança
                                1.1 -> densidade
                                1.2 -> senso de vizinhança, grupo economico dos vizinhos
                                1.3 -> atividades disponiveis (no futuro, facilities)
                                1.4 -> Uso da Terra ao redor
                                1.5 -> distancia de onde quer morar de fato
                                1.6 -> Tempo da area (visão do ambiente sendo degradado pelos habitantes)
                            2. grupo economico da celula
                            3. dar sensação de tempo, se é o primeiro passo, agente sabe de menos coisas
                                3.1 usar alguma variavel estocastica para realizar o "hiding" das info
                            4. variavel de pertubação aleatoria
                            5. Informações sobre outros agentes que estão desalocados e procurando
                            moradia ao redor de um raio do agente em questão

                            R = Isso deverá fazer com que o agente pense em ocupar uma celula a qual pode não
                            estar tão perto da ideal, porem no caminho da mesma (para quando n tiver chego nela)
                            Após chegar, será usado apenas para ver se ocupa ou não, pode ter uma variavel que
                            "sabe" se chegou na celula ideal
                            '''
                            # densidade alta, vizinhança cheia -> pobre, se tiver espaço fica, os demais se distanciam um pouco
                            if d > self.density:
                                if ag.economicGroup == 0:
                                    if self.grid[local[0]][local[1]].isOccupied() == None and self.grid[local[0]][local[1]].flag == 0:
                                        # self.grid[local[0]][local[1]].cellEcoGroup = ag.economicGroup
                                        self.grid[local[0]][local[1]].settle(ag)
                                        print('ocupei, linha 174 \tEconomic Now: ', ag.economicGroup)
                                        break

                                elif ag.economicGroup == 1:
                                    ag.walkSteps(self.grid, neigh, pos)

                                elif ag.economicGroup == 2:
                                    ag.walkSteps(self.grid, neigh, pos)

                            elif d <= self.density:                             #vizinhança não cheia, varios casos
                                # se o espaço não esta ocupado, ocupa, e defina o grupo economico da celula como sendo o do agente
                                if self.grid[local[0]][local[1]].isOccupied() == None and self.grid[local[0]][local[1]].flag == 0:
                                    # self.grid[local[0]][local[1]].cellEcoGroup = ag.economicGroup
                                    self.grid[local[0]][local[1]].settle(ag)
                                    print('ocupei, linha 188 \tEconomic Now: ', ag.economicGroup)
                                    break
                                # Casos para espaços/celulas ocupadas
                                else:
                                    # se eu for pobre, apenas ando
                                    if ag.economicGroup == 0:
                                        # self.walkSteps(ag, neigh)
                                        pass

                                    elif ag.economicGroup == 1: # se eu sou classe média, tem dois casos
                                        # se tiver um outro alguem da classe media, ou rico, eu ando
                                        # if self.grid[local[0]][local[1]].cellEcoGroup == 1 or self.grid[local[0]][local[1]].cellEcoGroup = 2 or self.grid[local[0]][local[1]].consolidate == True:
                                        #     # self.walkSteps(ag, neigh)
                                        #     pass
                                        if self.grid[local[0]][local[1]].cellEcoGroup == 0 and self.grid[local[0]][local[1]].consolidate == False and self.grid[local[0]][local[1]].flag == 0:
                                            agExpelled = self.evict(ag, local[0], local[1])
                                            agQueue.put(agExpelled)
                                            print('Expulsei, linha 206 \tEconomic Now: ', ag.economicGroup)
                                            break

                                    elif ag.economicGroup == 2: # se eu for rico
                                        if (self.grid[local[0]][local[1]].cellEcoGroup == 0 or self.grid[local[0]][local[1]].cellEcoGroup == 1) \
                                        and self.grid[local[0]][local[1]].consolidate == False and self.grid[local[0]][local[1]].flag == 0:
                                            agExpelled = self.evict(ag, local[0], local[1])
                                            agQueue.put(agExpelled)
                                            print('Expulsei, linha 215 \tEconomic Now: ', ag.economicGroup)
                                            break













######################## END #########################
