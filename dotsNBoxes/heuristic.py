import math
from .grid import Grid

class AI:
    def __init__(self, grid, states):
        self.min = float("-inf")
        self.max = float("-inf")
        self.states = self.generateStates(grid)

    def generateStates(self, grid):
        return []

    def miniMax(self, states, nodeOffset, maximizing, depth, targetDepth):
        #TODO
        if True:
            return states[nodeOffset]
        elif True:
            return min(miniMax(states, 0, False, depth, targetDepth))
        elif False:
            return max(miniMax(states, 0,  True, depth, targetDepth))
