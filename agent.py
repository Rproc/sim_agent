import numpy as np
import os
import random

class Agent:

    def __init__(self, economicGroup, allocated, steps, ideal=[]):
        self.economicGroup = economicGroup
        self.allocated = False
        self.steps = steps
        self.ideal = ideal
        # self.density = density


    def redCell(self, grid):

        center = [(ind, grid[ind].index(2)) for ind in xrange(len(grid)) if 2 in grid[ind]]

        seedValue = random.randrange(sys.maxsize)
        random.seed(seedValue)
        goal = random.choice(center)

        self.ideal = list(goal)



l = [['apple','banana','spoon'],['chair','table','spoon']]
def findItem(theList, item):
   return [(ind, theList[ind].index(item)) for ind in range(len(theList)) if item in theList[ind]]

findItem(l, 'apple') # [(0, 0)]
a= findItem(l, 'spoon') # [(1, 2)]

a = random.choice(a)
type(a)
list(a)
