#    *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#    |  Author:       D-U-C T-R-A-N      |
#    |  Carleton ID:  1-0-1-1-5-8-7-4-2  |
#    |  Created on:   08 - 17 - 2020     |
#    *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

import pygame, myModel

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
ORANGE = (184, 134, 11)
CREAM = (245,255,250)

class View:
    def __init__(self, height, cols, caption):
        self.height = height
        self.cols = cols
        self.caption = caption
        self.screen = pygame.display.set_mode((self.height, self.height))
        pygame.display.set_caption(self.caption)
        self.map = myModel.Map(cols, height)

    def getMap(self):
        return self.map

    def getSprites(self):
        return self.map.getSprites()

    def getClickedPixel(self, position):
        # This function determines the pixel at the clicked position
        y, x = position
        pixelSize = self.height // self.cols

        rowIndex = y // pixelSize
        colIndex = x // pixelSize

        pixel = self.map.getPixel(rowIndex, colIndex)
        return pixel

    def getInput(self):
        # This function displays a screen and ask for user's input
        import pygame.freetype
        pygame.init()

        window = pygame.display.set_mode((self.height, self.height))
        window.fill(BLACK)

        POKEFONT = pygame.freetype.Font("PokemonGB.ttf", 12)
        positions = [[50, 50], [75, 100], [75, 150], [75, 200]]
        lines = ["HOW ARE YOU PLANNING TO EXIT?", "1. DFS", "2. BFS", "3. A Star"]

        for line, pos in zip(lines, positions):
            text, rect = POKEFONT.render(line, WHITE)
            rect.topleft = pos
            window.blit(text, rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_1) or (event.key == pygame.K_KP1):
                        return 1
                    elif (event.key == pygame.K_2) or (event.key == pygame.K_KP2):
                        return 2
                    elif (event.key == pygame.K_3) or (event.key == pygame.K_KP3):
                        return 3

            self.update("getInput")

    def update(self, where):
        # This function helps with animations (sprites)
        if where == "main":
            self.screen.fill(BLACK)
            self.map.getSprites().draw(self.screen)
            pygame.display.flip()
            self.map.getSprites().update()

        elif where == "finalPath":
            self.screen.fill(BLACK)
            self.map.getSprites().draw(self.screen)
            pygame.display.flip()

        elif where == "getInput":
            pygame.display.update()

        elif where == "search":
            self.map.getSprites().update()
            self.map.getSprites().draw(self.screen)
            pygame.display.flip()
