from agent import Agent

class Cell:

    # occupied = with agent, x and y represents size and location of cell, flag means if the cell can be occupied
    def __init__(self, x, y, flag, cellEcoGroup, age, agent=None):
        # self.occupied = occupied
        self.x = x
        self.y = y
        self.flag = flag
        self.cellEcoGroup = cellEcoGroup
        self.age = age
        self.agent = agent
        self.consolidate = False


    def isOccupied(self):

        if cell.agent != None:
            return cell.agent
        else:
            return None


    def settle(self, agent):
        cell.agent = agent
        self.occupied = True
