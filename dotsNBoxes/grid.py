from random import randint


class Grid:
    def __init__(self, scale=75, clickRange=7):
        self.gridSize = 2
        self.tiles = None
        self.scale = scale
        self.clickRange = clickRange
        self.genBoardData()

    def genBoardData(self):
        self.tiles = self.genTiles()

    def genTiles(self):
        return [[Tile(self.scale, (x, y)) for x in range(0, self.gridSize)] for y in range(0, self.gridSize)]

    def resize(self, newSize):
        """
        Resize the board game, will reset tile values
        :param newSize: 1-5
        :return:
        """
        # Update grid size
        self.gridSize = int(newSize)
        # Update rest of board data
        self.genBoardData()

    def isConquered(self):
        return self.tiles[0][0].conquered

    def getTileConq(self):
        """
        Returns all tiles' conquered values
        :return: list of conquered boolean
        """
        tileConquered = [[self.tiles[x][y].conquered for x in range(0, self.gridSize)] for y in range(0, self.gridSize)]
        return tileConquered

    def getTileVals(self):
        tileVals = [[self.tiles[x][y].val for x in range(0, self.gridSize)] for y in range(0, self.gridSize)]
        return tileVals

    def getTileEdges(self):
        tileEdges = [[self.tiles[x][y].edges for x in range(0, self.gridSize)] for y in range(0, self.gridSize)]
        return tileEdges

class Tile:
    def __init__(self, scale, startCoord=(0, 0)):
        """
        Has data whether it is conquered, it's value,
        and edges associated to the tile (will overlap with other tiles)
        :param startCoord:
        """
        self.conquered = False
        self.val = randint(1, 5)
        # Reference to the upper left
        # coordinate of the tile
        self.startCoord = startCoord
        self.scale = scale
        self.edges = self.initEdges()

    def initEdges(self):
        """
        This method returns a list of edges, where each edge is a list of 2 tuples.
        Eg: An edge is defined by points [(x1, y1), (x2, y2)] If the an edge is null
        it has already been clicked on and can no longer be used by the AI or player

        It is also scaled to what the grid scale is set to default is set to 75px

        :return:
        """
        x, y = [self.startCoord[0] * self.scale, self.startCoord[1] * self.scale]
        # Offset of +1 * self.scale
        x1, y1 = [(x+self.scale), (y+self.scale)]

        return [[(x, y), (x1, y), None],
                [(x1, y), (x1, y1), None],
                [(x1, y1), (x, y1), None],
                [(x, y1), (x, y), None]]
