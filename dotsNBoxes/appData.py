from .grid import Grid


class Data:

    def __init__(self):
        self.AIScore = 0
        self.playerScore = 0
        # This will change to true until the board is actually rendered
        # in dotsNBoxes.js see windowResized
        self.inSession = False
        self.currentTurn = 'player'
        self.gridSpace = Grid()

    def updateGridSize(self, newSize):
        # Update grid size
        self.gridSize = self.gridSpace.resize(int(newSize))

    def getGridSize(self):
        return self.gridSpace.gridSize

    def jsonifyTiles(self):
        tiles = [[{'conquered': self.gridSpace.getTileConq()[x][y],
                   'value': self.gridSpace.getTileVals()[x][y],
                   'edges': self.gridSpace.getTileEdges()[x][y]
                   }for x in range(0, self.getGridSize())
                  ]for y in range(0, self.getGridSize())]
        return tiles

    def getTiles(self):
        return self.gridSpace.tiles

    def requestEdge(self, coord):
        """
        Checks all edges
        :param coord:
        :return:
        """
        for row in self.gridSpace.getTileEdges():
            for tile in row:
                for edge in tile:
                    if edge[2] is None and self.isWithinRange(edge, coord):
                        return True
        return False

    def isWithinRange(self, edge, coord):
        # TODO PROBLEM WITH BOUNDING BOX
        # move to tile class??
        loBoundX = edge[0][0] - self.gridSpace.clickRange
        hiBoundX = edge[1][0] + self.gridSpace.clickRange
        loBoundY = edge[0][1] - self.gridSpace.clickRange
        hiBoundY = edge[1][1] + self.gridSpace.clickRange
        if (loBoundX < coord[0] < hiBoundX and loBoundY < coord[1] < hiBoundY):
            # make it unavailable
            edge[2] = self.currentTurn
            return True
        else:
            return False

    def initAI(self):
        print('call AI')

    def getScale(self):
        return self.gridSpace.scale
