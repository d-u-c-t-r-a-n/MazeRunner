#    *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#    |  Author:       D-U-C T-R-A-N      |
#    |  Carleton ID:  1-0-1-1-5-8-7-4-2  |
#    |  Created on:   08 - 17 - 2020     |
#    *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

import pygame
import queue as q

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
ORANGE = (184, 134, 11)
CREAM = (245,255,250)

class Pixel(pygame.sprite.Sprite):
    def __init__(self, row, col, height, numCols):
        super().__init__()
        self.row = row
        self.col = col
        self.height = height
        self.size = self.height
        self.locAdjuster = self.size//2
        self.velocity = 1
        self.animation = False
        self.animationRound = 1

        self.numCols = numCols
        self.x = row * height
        self.y = col * height
        self. neighbors = list()
        self.color = BLACK
        self.id = None

        self.image = pygame.Surface((self.height, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def getPosition(self):
        return (self.row, self.col)

    def isStart(self):
        return self.color == BLUE

    def isEnd(self):
        return self.color == PURPLE

    def isWall(self):
        return self.color == ORANGE

    def reset(self):
        self.color = BLACK
        self.size = self.height
        self.locAdjuster = self.size // 2
        self.velocity = 1

    def setStart(self):
        self.color = BLUE

    def setEnd(self):
        self.color = PURPLE

    def setWall(self):
        self.color = ORANGE

    def setOpen(self):
        self.color = RED

    def setClose(self):
        self.color = GREEN

    def setPath(self):
        self.color = WHITE

    def setId(self, value):
        self.id = value

    def setChecking(self):
        self.color = CREAM
        self.animation = True

    def setNeighbors(self, map):
        self.neighbors = list()

        # LEFT
        if self.col > 0 and not map[self.row][self.col - 1].isWall():
            self.neighbors.append(map[self.row][self.col - 1])

        # UP
        if self.row > 0 and not map[self.row - 1][self.col].isWall():
            self.neighbors.append(map[self.row - 1][self.col])

        # RIGHT
        if self.col < self.numCols - 1 and not map[self.row][self.col + 1].isWall():
            self.neighbors.append(map[self.row][self.col + 1])

        # DOWN
        if self.row < self.numCols - 1 and not map[self.row +1][self.col].isWall():
            self.neighbors.append(map[self.row +1][self.col])

    def __lt__(self, other):
        return (self.id < other.id)

    def clearAnimation(self):
        self.animation = False

    def update(self):

        if self.isStart() or self.isEnd() or self.isWall():
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
            self.rect.x = self.x + self.locAdjuster
            self.rect.y = self.y + self.locAdjuster

            if self.size >= self.height + 1:
                self.size = self.height
                self.rect.x = self.x
                self.rect.y = self.y
                self.locAdjuster = 0
            elif self.size > 2:
                self.size -= (2 * self.velocity)
                self.locAdjuster += (1 * self.velocity)
            else:
                self.size += 2
                self.locAdjuster -= 1
                self.velocity *= -1

        elif self.animation:
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill(BLACK)
            self.circleRect = pygame.draw.circle(self.image, GREEN, (self.size//2,self.size//2), self.animationRound)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.animationRound += 1
        else:
            self.image = pygame.Surface((self.height, self.height))
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

class Map:
    def __init__(self, numCols, mapHeight):
        self.numCols = numCols
        self.mapHeight = mapHeight
        self.map = list()
        self.pixelSize = mapHeight // numCols
        self.sprites = pygame.sprite.Group()
        self.started = False #algorithm started
        self.startPixel = None
        self.endPixel = None
        self.walls = None

        # Initialize Pixels
        for rowIndex in range (self.numCols):
            self.map.append(list())
            for colIndex in range(self.numCols):
                self.map[rowIndex].append(Pixel(rowIndex, colIndex, self.pixelSize, self.numCols))

        # Initialize Animation
        for row in self.map:
            for pixel in row:
                self.sprites.add(pixel)

    def reset(self):
        self.map = list()
        self.sprites = pygame.sprite.Group()
        self.startPixel = None
        self.endPixel = None
        self.started = False

        # Reset Pixels
        for rowIndex in range(self.numCols):
            self.map.append(list())
            for colIndex in range(self.numCols):
                self.map[rowIndex].append(Pixel(rowIndex, colIndex, self.pixelSize, self.numCols))

        # Reset Animation
        for row in self.map:
            for pixel in row:
                self.sprites.add(pixel)

    def getMap(self):
        return self.map

    def getSprites(self):
        return self.sprites

    def getPixel(self, row, col):
        return self.map[row][col]

    def getStart(self):
        return self.startPixel

    def getEnd(self):
        return self.endPixel

    def getStarted(self):
        return self.started

    def setStarted(self):
        self.started = True

    def setStart(self, startPixel):
        self.startPixel = startPixel
        self.startPixel.setStart()

    def setEnd(self, endPixel):
        self.endPixel = endPixel
        self.endPixel.setEnd()

    def clearStart(self):
        self.startPixel.reset()
        self.startPixel = None

    def clearEnd(self):
        self.endPixel.reset()
        self.endPixel = None

    def setNeighbors(self):
        for col in self.map:
            for pixel in col:
                pixel.setNeighbors(self.map)

    def search(self, userInput, view):
        # This function performs search algorithm
        origination = dict()

        def regSearch(view, map, startPixel, endPixel, bfs = False):
            queueTemp = {0}  # To determine if a pixel is in the original queue
            if bfs:
                queue = q.Queue()
            else:
                queue = q.LifoQueue()

            queue.put((0, startPixel))

            score = {pixel: float("inf") for row in map for pixel in row}
            score[startPixel] = 0

            while not queue.empty():

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                currentPixel = queue.get()[1]

                if currentPixel in queueTemp:
                    continue

                queueTemp.add(currentPixel)
                if currentPixel is not startPixel:
                    currentPixel.setChecking()

                if currentPixel == endPixel:  # Path found
                    finalPath(view, endPixel, origination)
                    startPixel.setEnd()
                    endPixel.setEnd()
                    return True

                for neighbor in currentPixel.neighbors:
                    scoreTemp = score[currentPixel] + 1

                    if scoreTemp < score[neighbor]:
                        score[neighbor] = scoreTemp
                        origination[neighbor] = currentPixel

                    if neighbor not in queueTemp:
                        queue.put((score[neighbor], neighbor))

                view.update("search")

                if currentPixel != startPixel:
                    currentPixel.setClose()

        def aStarSearch(view, map, startPixel, endPixel):
            fScoreStartPixel = 0
            id = 0  # Keep track of which pixel got added first
            queue = q.PriorityQueue()
            queueTemp = {startPixel}  # To determine if a pixel is in the original queue

            gScore = {pixel: float("inf") for row in map for pixel in row}
            gScore[startPixel] = 0
            fScore = {pixel: float("inf") for row in map for pixel in row}
            fScore[startPixel] = manhattanHeuristic(startPixel.getPosition(), endPixel.getPosition())

            queue.put((fScoreStartPixel, startPixel))

            while not queue.empty():

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                currentPixel = queue.get()[1]  # Get the pixel with lowest F-score in the queue
                queueTemp.remove(currentPixel)
                if currentPixel is not startPixel:
                    currentPixel.setChecking()

                if currentPixel == endPixel:  # Path found
                    finalPath(view, endPixel, origination)
                    startPixel.setEnd()
                    endPixel.setEnd()
                    return True

                for neighbor in currentPixel.neighbors:
                    gScoreTemp = gScore[currentPixel] + 1

                    if gScoreTemp < gScore[neighbor]:
                        gScore[neighbor] = gScoreTemp
                        fScore[neighbor] = gScoreTemp + manhattanHeuristic(neighbor.getPosition(),
                                                                           endPixel.getPosition())
                        origination[neighbor] = currentPixel

                        if neighbor not in queueTemp:
                            id += 1
                            neighbor.setId(id)
                            queue.put((fScore[neighbor], neighbor))
                            queueTemp.add(neighbor)

                view.update("search")

                if currentPixel != startPixel:
                    currentPixel.setClose()

        def finalPath(view, currentPixel, origination):
            # This function displays the estimated shortest path
            while currentPixel in origination:
                currentPixel = origination[currentPixel]
                currentPixel.clearAnimation()
                currentPixel.setPath()

                view.update("finalPath")

        def manhattanHeuristic(a, b):
            x1, y1 = a
            x2, y2 = b
            return abs(x2 - x1) + abs(y2 - y1)

        if userInput == 1:
            regSearch(view, self.map, self.startPixel, self.endPixel)
        elif userInput == 2:
            regSearch(view, self.map, self.startPixel, self.endPixel, bfs = True)
        elif userInput == 3:
            aStarSearch(view, self.map, self.startPixel, self.endPixel)