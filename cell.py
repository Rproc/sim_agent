from agent import Agent

class Cell:

    # occupied = with agent, x and y represents size and location of cell, flag means if the cell can be occupied
    def __init__(self, x, y, flag, cellEcoGroup, age, facilities, agent=None):
        # self.occupied = occupied
        self.x = x
        self.y = y
        self.flag = flag
        self.cellEcoGroup = cellEcoGroup
        self.age = age
        self.agent = agent
        self.consolidate = False
        self.facilities = facilities


    def isOccupied(self):

        if self.agent != None:
            return self.agent
        else:
            return None


    def settle(self, agent):
        self.agent = agent
        agent.allocated = True
        # self.age += 1
        # self.cellEcoGroup = agent.economicGroup
