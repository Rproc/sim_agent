from cell import Cell
from model import Model
# economicGroup, agent settled, number in space (x,y)

consolidationTime = 5
decay = 8

mapGrid = Model(consolidationTime, decay)
# print(mapGrid[0][2])

tab = Cell(mapGrid, consolidationTime, decay)
