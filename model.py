from cell import Cell
from agent import Agent
import math
import random
import sys
from collections import deque, Counter, OrderedDict
import queue
from statistics import mean
import monteCarlo as mc
class Model:


    def __init__(self, numberAgents, divisionAgents, consolidationTime, decayStartPoint, density, grid, alpha, threshold, facilities=[], total_facilities=0):

        self.numberAgents = numberAgents
        self.divisionAgents = divisionAgents
        self.consolidationTime = consolidationTime
        self.decayStartPoint = decayStartPoint
        self.density = density
        self.grid = grid
        self.facilities = facilities
        self.total_facilities = total_facilities
        self.alpha = alpha
        self.threshold = threshold

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
            if mc.crude_monte_carlo() > 0.7:
                self.grid[i][j].cellEcoGroup -= 1
                self.grid[i][j].aged = True

        if self.grid[i][j].age >= self.decayStartPoint and self.grid[i][j].cellEcoGroup == 2:
            d, a0, a1, a2, a3, a4 = self.neighborhood(neigh, i, j, len(self.grid[0]))
            # if greater, abandon cell
            if d >= density:
                self.grid[i][j].agent.allocated = False
                self.grid[i][j].agent = None

        if self.grid[i][j].agent != None:
            self.grid[i][j].age += 1

    def neighborhood(self, neigh, ag, i, j, row, scope=2, radius=1):

        # sys.exit(0)
        newGrid, gFac = ag.agentVisionQT(self.grid, scope, radius)
        newCeg = []
        if neigh == 'moore':

            coordinates = [[i-1, j], [i-1, j+1], [i, j+1], [i+1, j+1], [i+1, j], [i+1, j-1], [i, j-1], [i-1, j-1]]

            near = 0
            ceg = []
            aeg = []
            facN = []
            cellConsolidated = 0

            for (x, y) in coordinates:
                if (x < 0 or y < 0) or (x >= len(self.grid) or y >= len(self.grid[0])):
                    pass
                else:
                    if self.grid[x][y].agent != None:
                        near+=1
                        aeg.append(self.grid[x][y].agent.economicGroup)
                    ceg.append(self.grid[x][y].cellEcoGroup)
                    newCeg.append(newGrid[x][y])
                    facN.append(len(self.grid[x][y].facilities))
                    if self.grid[x][y].consolidate:
                        cellConsolidated+=1

        return near, ceg, aeg, facN, newCeg, cellConsolidated

    def createAgents(self, steps):

        groupZero = math.floor(self.numberAgents * self.divisionAgents[0]) # Low Economics
        groupOne = math.floor(self.numberAgents * self.divisionAgents[1]) # Mid Economics
        groupTwo = math.floor(self.numberAgents * self.divisionAgents[2]) # High Economics

        ag = [groupZero, groupOne, groupTwo]
        # print(ag)
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

    def decay(self, start, half_life, length):
        coef = math.exp(-math.log(2)/half_life)
        return list(map(lambda t: start * coef ** t, range(length) ))

    def eval(self, neigh, pos, ag, timeOfSim, scope, distToRedCell, flags, radius=1):

        '''
        density:        min = 0, max = 8                depends on the agent economicGroup
        ecoGroupCell:   most frequent (or weights)      value increase with the high value of eco cell
        ecoGroupAg:     most frequent                   value increase with the same economicGroup of agent x
        facN:           mean of facilities in neigh     higher the better
        newCeg:         most frequent (#2 with mask)    higher the better
        distToRedCell:  distant to cell X               lower the better
        timeOfSim:      the area attractiveness decay*  lower the better
        alpha:          has the objective of control    ---


        * if cell were occupied enough time
        '''
        # ag.pos = pos

        # mudar para o newGrid, calcular ele e mascarar Informações
        density, ecoGroupCell, ecoGroupAg, facN, newCeg, cellConsolidated = self.neighborhood(neigh, ag, pos[0], pos[1], len(self.grid[0]), scope=scope, radius=radius)
        suitability = 1 if ag.economicGroup >= self.grid[pos[0]][pos[1]].cellEcoGroup else 0

        if suitability == 1:
        # density (between 0 and 1)
            if density == 0:
                d = 1
            elif density <= 3:
                d = 0.75
            elif density > 3 and density < 6:
                d = 0.5
            elif density >= 6 and density <= 8:
                d = 0.25
            else:
                d = 0.1

            if flags[0] == 0:
            # grupo economico das celulas vizinhas (fazer por porcentagem da maior) entre 0 e 1
                ecoCellViz = Counter(ecoGroupCell)
                ecoCellViz = OrderedDict(sorted(ecoCellViz.items()))
                cellViz = []
                for key, value in ecoCellViz.items():
                    cellViz.append(value)

                g = self.cellsNeigh(cellViz, ag, cellConsolidated)
            else:
                # grupo economico das celulas vizinhas (fazer por porcentagem da maior) entre 0 e 1
                # sem ter muito conhecimento sobre os arredores
                ecoCellMasked = Counter(newCeg)
                ecoCellMasked = OrderedDict(sorted(ecoCellMasked.items()))
                cellVizMasked = []
                for key, value in ecoCellMasked.items():
                    cellVizMasked.append(value)

                g = self.cellsBlurred(cellVizMasked, ag)


            # grupo economico dos agentes alocados nas celulas vizinhas, fazer o mesmo caso da de cima
            if (ecoGroupAg != []):
                ecoAgViz = Counter(ecoGroupAg)
                ecoAgViz = OrderedDict(sorted(ecoAgViz.items()))
                agViz = []
                for key, value in ecoAgViz.items():
                    agViz.append(value)
            else:
                agViz = [0, 0, 0]

            facN = [i/self.total_facilities for i in facN]
            # comodidades -> entre 0 e 1, 1 tendo todas as disponiveis nas imediações da celula
            numberFacilitesAround = mean(facN)
            # print(numberFacilitesAround/self.total_facilities)

            # distancia da celula, quanto mais distante, tem que pesar mais
            try:
                distPath = abs(0.99-distToRedCell/len(ag.path))
            except ZeroDivisionError:
                decayList = self.decay(1, 1, 5)
                decayList.reverse()
                try:
                    distPath = decayList[ag.walkedSteps]
                except IndexError:
                    distPath = decayList[-1]


            # tempo de simulação, quanto maior, menos atrativo fica a area, se essa celula ja tiver ocupada
            # timeOfSim
            ambienceAttractiveness = self.grid[pos[0]][pos[1]].age/(timeOfSim+2)

            print('\n---------------------------------')
            print('atract:', (1-ambienceAttractiveness))
            print('fac: ', numberFacilitesAround)
            print('distPath: ', (distPath))
            print('cells: ', g)
            print('density: ', d)

            indexOccup = (d)*(1 - ambienceAttractiveness)*numberFacilitesAround
            indexOccup *= (distPath)*g*self.alpha
            print('occup?: ', indexOccup)

        else:
            indexOccup = 0
            print('\n===============================')
            print('cannot settle\n')
            print('===============================')


        return density, indexOccup

    def cellsNeigh(self, cellViz, ag, cellConsolidated):

        n = 0
        for i in range(0, len(cellViz)):
            if ag.economicGroup >= i:
                n += cellViz[i]

        n = n/len(cellViz)
        c = cellConsolidated/len(cellViz)

        if ag.economicGroup == 0:
            n = n + c
        else:
            n = n - c

        return min(1, n)

    def cellsBlurred(self, cellVizMasked, ag):

        n = 0
        for i in range(0, len(cellVizMasked)):
            if ag.economicGroup >= i:
                n += cellVizMasked[i]

        n = n/len(cellVizMasked)
        # c = cellConsolidated/len(cellViz)

        # if ag.economicGroup == 0:
        #     n = n + c
        # else:
        #     n = n - c

        return min(1, n)

    # def cellsNeighOld (cellViz, ag, cellConsolidated):
        # cellPred = cellViz.index(max(cellViz))
        # n = (max(cellViz)/len(cellViz))
        # if cellPred == ag.economicGroup:
        #     if ag.economicGroup == 0 and cellConsolidated > 0:
        #         return min(1, n*cellConsolidated)
        #     elif ag.economicGroup == 2:
        #         return 1
        #     else:
        #         return n
        #
        # elif cellConsolidated >= max(cellViz)
        #     if ag.economicGroup == 2:
        #         return 0
        # else:
        #     return (cellViz[ag.economicGroup]/len(cellViz))

    def agentsNeigh(self, ag, agViz):

        agMax = agViz.index(max(agViz))
        n = (max(agViz)/len(agVizV))
        m = 0
        fator = 1

        if ag.economicGroup == agMax:
            fator += 0.5
        if agViz[2] > 0:
            fator = agViz[2]
        else:
            return min(1, n*fator)

    def evict(self, ag, x, y, scope):
        agExpelled = self.grid[x][y].agent
        agExpelled.allocated = False
        agExpelled.redCellInt(self.grid, self.total_facilities, scope)
        self.grid[x][y].age = 1

        self.grid[x][y].settle(ag)

        return agExpelled

    def simulation(self, neigh, timeOfSim, steps, flags, radius):

        l = self.createAgents(steps)
        agQueue = queue.Queue()
        hist = []

        for t in range(0, timeOfSim):
            print('time: ', t)

            if t < 2:
                scope = 2
            if t >= 2 and t < 4:
                scope = 4
            else:
                scope = len(self.grid)

            #first do things with cells
            for i in range(0, len(self.grid)):
                for j in range(0, len(self.grid[0])):
                    if (t > 1):
                        self.periferization(neigh, i, j)

            # prepare the agents
            for elem in l:
                agQueue.put(elem)

            # while someone not fixed in a cell
            while not agQueue.empty():

                ag = agQueue.get()
                if t == 0:
                    pos = ag.randomWalk(self.grid)
                    path_to_ideal = ag.walkToRedCell(self.grid, pos)

                if t > 1 and ag.allocated == False:
                    ag.redCellInt(self.grid, self.total_facilities, scope)
                    path_to_ideal = ag.walkToRedCell(self.grid, pos)

                while (ag.allocated == False):
                    if len(path_to_ideal) > 0:
                        x, y = path_to_ideal.pop(0)
                        local = [x, y]
                        ag.pos = local
                        # print('hey')
                    else:
                        local = ag.walkSteps(self.grid, neigh)
                    # vision, in the future, or something that will compose the vision
                    d, indexOccup = self.eval(neigh, local, ag, timeOfSim, scope, len(path_to_ideal), flags, radius)
                    hist.append(indexOccup)
                    # sys.exit(0)
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
                    d = d/8
                    # densidade alta, vizinhança cheia -> pobre, se tiver espaço fica, os demais se distanciam um pouco
                    if d - indexOccup > self.density :
                        if ag.economicGroup == 0:
                            if self.grid[local[0]][local[1]].isOccupied() == None and self.grid[local[0]][local[1]].flag == 0:
                                # self.grid[local[0]][local[1]].cellEcoGroup = ag.economicGroup
                                self.grid[local[0]][local[1]].settle(ag)
                                # print('in d>den, ag.eco = 0 -- allocated: ', ag.allocated)
                                # print('ocupei, linha 174 \tEconomic Now: ', ag.economicGroup)
                                break

                        elif ag.economicGroup == 1:
                            ag.walkSteps(self.grid, neigh)

                        elif ag.economicGroup == 2:
                            ag.walkSteps(self.grid, neigh)

                    elif d <= self.density:                             #vizinhança não cheia, varios casos
                        # se o espaço não esta ocupado, ocupa, e defina o grupo economico da celula como sendo o do agente
                        if self.grid[local[0]][local[1]].isOccupied() == None and self.grid[local[0]][local[1]].flag == 0:
                            # self.grid[local[0]][local[1]].cellEcoGroup = ag.economicGroup
                            if ag.economicGroup == 2 and self.grid[local[0]][local[1]].aged == True:
                                pass
                            else:
                                self.grid[local[0]][local[1]].settle(ag)
                            # print('In d<= den, allocated: ', ag.allocated)

                            # print('ocupei, linha 188 \tEconomic Now: ', ag.economicGroup)
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
                                    agExpelled = self.evict(ag, local[0], local[1], scope)
                                    # print('Expulsei, eco 1 \tEconomic Now: ', ag.economicGroup)
                                    # print('agExp allocation: ', agExpelled.allocated)
                                    # print('subs alloc: ', ag.allocated)
                                    agQueue.put(agExpelled)
                                    break

                            elif ag.economicGroup == 2: # se eu for rico
                                if (self.grid[local[0]][local[1]].cellEcoGroup == 0 or self.grid[local[0]][local[1]].cellEcoGroup == 1) \
                                and self.grid[local[0]][local[1]].consolidate == False and self.grid[local[0]][local[1]].flag == 0 \
                                and self.grid[local[0]][local[1]].aged == False:
                                    agExpelled = self.evict(ag, local[0], local[1], scope)
                                    agQueue.put(agExpelled)
                                    # print('Expulsei, eco 2 \tEconomic Now: ', ag.economicGroup)
                                    # print('agExp allocation: ', agExpelled.allocated)
                                    # print('subs alloc: ', ag.allocated)
                                    break

        return hist











######################## END #########################
