#    *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
#    |  Author:       D-U-C T-R-A-N      |
#    |  Carleton ID:  1-0-1-1-5-8-7-4-2  |
#    |  Created on:   08 - 17 - 2020     |
#    *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

# This application visualizes different types
# of path finding algorithm

import pygame, myView

def main():
    HEIGHT = 500
    COLS = 50
    CAPTION = "MAZE RUNNER"
    view = myView.View(HEIGHT, COLS, CAPTION)
    myMap = view.getMap()

    run = True #running the main loop

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0] and not myMap.getStarted(): # If click the left mouse
                pixel = view.getClickedPixel(pygame.mouse.get_pos())
                if myMap.getStart() == None and pixel != myMap.getEnd(): # avoid putting start and end point on each other
                    myMap.setStart(pixel)
                elif myMap.getEnd() == None and pixel != myMap.getStart(): # avoid putting start and end point on each other
                    myMap.setEnd(pixel)

                # MODIFY (UNCOMMENT BELOW) IF ADD PREDEFINED MAZE
                elif pixel != myMap.getStart() and pixel != myMap.getEnd():
                    pixel.setWall()
                    # myMap.setWalls()

            elif pygame.mouse.get_pressed()[2] and not myMap.getStarted(): # If click the right mouse
                pixel = view.getClickedPixel(pygame.mouse.get_pos())
                if pixel == myMap.getStart(): myMap.clearStart()
                if pixel == myMap.getEnd(): myMap.clearEnd()
                pixel.reset()

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN) and not myMap.getStarted() and myMap.getStart() != None and myMap.getEnd() != None:
                    myMap.setStarted()
                    myMap.setNeighbors()
                    myMap.getStart().clearAnimation()  # Let the startPixel has different colour than setChecking colour
                    myMap.search(view.getInput(), view)

                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE or event.key == pygame.K_ESCAPE:
                    myMap.reset()

        view.update("main")

    pygame.quit()

if __name__ == "__main__":
    main()
