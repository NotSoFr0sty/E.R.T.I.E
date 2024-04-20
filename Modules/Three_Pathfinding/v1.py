'''
A* Pathfinding Algorithm:

OPEN //set of nodes to be evaluated
CLOSED //set of nodes already evaluated (potential path)
add the start node to OPEN

loop
    current = node in OPEN with the lowest fCost
    remove current from OPEN
    add current to CLOSED

    if current is the goal node //path has been found
        return
    
    for each neighbor of the current node
        if neighbor is not traversable or neighbor is in CLOSED
            skip to next neighbor
        
        if neighbor is not in OPEN || new path to neighbor is shorter
            set parent of neighbor to current #I swapped this line and the next line.
            set fCost of neighbor #I swapped this line and the previous line.
            if neighbor is not in OPEN
                add neighbor to OPEN
'''
'''
For Test1.py
Open the testFP
Start node is top-left corner pixel
Goal node is bottom-right corner pixel
NOTE: Black means wall, white means floor
'''

import cv2 as cv
import numpy as np
import time
import sys 
import os
# sys.path.append(os.path.abspath("Modules/1_ImageProcessing"))
# from One_ImageProcessing.ImageProcessing import floorPlanNum

def main():
    class Node:
        '''Each object of this class represents a pixel.'''

        def __init__(self, coords):
            '''coords is a list of the form [x,y]'''

            self.coords = coords
            self.xCoord = self.coords[0]
            self.yCoord = self.coords[1]
            self.pixelColor = img[self.xCoord, self.yCoord]
            self.fCost = 1000000
        
        def __str__(self):
            return ','.join(str(x) for x in self.coords)

        def __lt__(self, other):
            '''Allows the sorted() function to sort nodes by fCost'''

            return self.fCost < other.fCost
        
        def isTraversable(self):
            '''Returns True if the pixel corresponding to the node is white'''

            if self.pixelColor == 255: return True
            else: return False

        def setParent(self, parent):
            self.parent = parent

        def calcAdjacencyTo(self, tgtNode):
            '''Returns 'x' if the node is diagonally adjacent to the target node, else returns '+' '''

            xCoord = self.xCoord
            yCoord = self.yCoord
            node = tgtNode
            if node.xCoord == xCoord-1 and node.yCoord == yCoord: # top
                return '+'
            if node.xCoord == xCoord-1 and node.yCoord == yCoord+1: # top right
                return 'x'
            if node.xCoord == xCoord and node.yCoord == yCoord+1: # right
                return '+'
            if node.xCoord == xCoord+1 and node.yCoord == yCoord+1: # bottom right
                return 'x'
            if node.xCoord == xCoord+1 and node.yCoord == yCoord: # bottom
                return '+'
            if node.xCoord == xCoord+1 and node.yCoord == yCoord-1: # bottom left
                return 'x'
            if node.xCoord == xCoord and node.yCoord == yCoord-1: # left
                return '+'
            if node.xCoord == xCoord-1 and node.yCoord == yCoord-1: # top left
                return 'x'


        def calcGCost(self):
            '''Sets the node's gCost, which is the distance from the start node.'''

            adj = self.calcAdjacencyTo(self.parent)
            if adj == '+':
                self.gCost = 10 + self.parent.gCost
            if adj == 'x':
                self.gCost = 14 + self.parent.gCost

        def calcHCost(self):
            '''Sets the node's hCost, which is the distance to the goal node.'''

            xCoord = self.xCoord
            yCoord = self.yCoord
            goalNode = findNodeHavingCoords(goal) # sets goal node
            x = abs(goalNode.xCoord - xCoord)
            y = abs(goalNode.yCoord - yCoord)
            if x<y: # x is smaller than y
                self.hCost = 14*x + 10*(y-x)
            else: # y is smaller than x
                self.hCost = 14*y + 10*(x-y)


        def calcFCost(self):
            '''Sets the nodes fCost.
                fCost = gCost + hCost'''

            self.calcGCost()
            self.calcHCost()
            self.fCost = self.gCost + self.hCost


    def findNodeHavingCoords(coords):
        '''Returns the node in the list "nodes" which has the coordinates "coords." '''

        x = coords[0]
        y = coords[1]
        oneD = (x * cols) + y
        return nodes[oneD]

    def getNeighbors(centerNode):
        '''Returns a list of adjacent nodes of the input node'''
        # neighbors = []
        # xCoord = centerNode.xCoord
        # yCoord = centerNode.yCoord
        # for node in nodes:
        #     if node.xCoord == xCoord-1 and node.yCoord == yCoord: # top
        #         neighbors.append(node)
        #     if node.xCoord == xCoord-1 and node.yCoord == yCoord+1: # top right
        #         neighbors.append(node)
        #     if node.xCoord == xCoord and node.yCoord == yCoord+1: # right
        #         neighbors.append(node)
        #     if node.xCoord == xCoord+1 and node.yCoord == yCoord+1: # bottom right
        #         neighbors.append(node)
        #     if node.xCoord == xCoord+1 and node.yCoord == yCoord: # bottom
        #         neighbors.append(node)
        #     if node.xCoord == xCoord+1 and node.yCoord == yCoord-1: # bottom left
        #         neighbors.append(node)
        #     if node.xCoord == xCoord and node.yCoord == yCoord-1: # left
        #         neighbors.append(node)
        #     if node.xCoord == xCoord-1 and node.yCoord == yCoord-1: # top left
        #         neighbors.append(node)
        # return neighbors

        neighbors = []
        x = centerNode.xCoord
        y = centerNode.yCoord
        try:
            if x-1<0: raise IndexError
            coords = [x-1, y]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            if x-1<0: raise IndexError
            temp = img[x-1, y+1]
            coords = [x-1, y+1]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            temp = img[x, y+1]
            coords = [x, y+1]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            temp = img[x+1, y+1]
            coords = [x+1, y+1]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            temp = img[x+1, y]
            coords = [x+1, y]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            if y-1<0: raise IndexError
            temp = img[x+1, y-1]
            coords = [x+1, y-1]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            if y-1<0: raise IndexError
            temp = img[x, y-1]
            coords = [x, y-1]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            if y-1<0 or x-1<0: raise IndexError
            temp = img[x-1, y-1]
            coords = [x-1, y-1]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass

        return neighbors

    def isNewPathShorter(node, current):
        '''Returns True if the node's gCost to "current" is less than its gCost'''

        if node not in open:
            return False
        oldGCost = node.gCost
        adj = node.calcAdjacencyTo(current)
        if adj == '+':
                newGCost = 10 + current.gCost
        if adj == 'x':
                newGCost = 14 + current.gCost
        if newGCost < oldGCost:
            return True

    def getPath(coords):
        '''Returns a list with all nodes on the path.
        The path is from the node with coordinates "coords" to the start node.'''
        pathNodes = []
        node = findNodeHavingCoords(coords)
        while(node.parent != node):
            pathNodes.append(node)
            node = node.parent
        pathNodes.append(node)
        return pathNodes

    def drawPath(pathNodes, img):
        '''Draws a path on the input image and returns the resulting image.
        All pixels that correspond to the nodes in the input list will be colored red.
        '''
        img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        # for x in range(rows):
        #     for y in range(cols):

        #         for node in nodes:
        #             if node.coords == [x,y]:
        #                 # color that pixel red
        #                 img[x,y] = [0,0,255]
        for node in pathNodes:
            img[node.xCoord, node.yCoord] = [0,0,255]
        return img

    def overlayPath(img, fp):
        
        # scale new image to match ogFPImg
        shapeIWant = []
        shapeIWant.append(fp.shape[1])
        shapeIWant.append(fp.shape[0])
        shapeIWant = tuple(shapeIWant)
        img = cv.resize(img, shapeIWant, interpolation=cv.INTER_NEAREST)

        # fp = cv.addWeighted(img, .3, fp, .7, 0)
        # return fp

        for x in range(ogRows):
            for y in range(ogCols):
                
                if (img[x,y] == [0,0,255]).all(): #if pixel is red
                    fp[x,y] = [0,0,255]
        return fp

    def onMouse(event, x, y, flags, param):
        global mousePos
        if event == cv.EVENT_LBUTTONDOWN:
            x, y = y, x
            mousePos = [x,y]
            cv.destroyWindow(globalLabel)
            # print(f'{mousePos}\tPress any key to confirm...')

    def setPosWithMouse(img, label):
        '''Returns the position of the cursor when LeftButton is pressed.'''
        
        global globalLabel
        globalLabel = f'Set {label}\'s position'
        cv.imshow(f'Set {label}\'s position', img)
        cv.setMouseCallback(f'Set {label}\'s position', onMouse)
        cv.waitKey(0)
        # cv.destroyWindow(f'Set {label}\'s position')
        try:
            mousePos[0] = round(mousePos[0]*0.3)
            mousePos[1] = round(mousePos[1]*0.3)
        except NameError:
            print("Failed to set position, exiting...")
            raise SystemExit
        return mousePos

    floorPlanNum = 2
    # read testFP in grayscale mode #FIXME: Comments are out of date.
    originalFPImg = cv.imread(f'Floorplans/{floorPlanNum}.jpg')
    ogRows = originalFPImg.shape[0]
    ogCols = originalFPImg.shape[1]
    inputImg = cv.imread('Floorplans/Output.png', cv.IMREAD_GRAYSCALE)
    inputImg = cv.bitwise_not(inputImg) # inverted original image
    img = cv.resize(inputImg, (0,0), fx=0.30, fy=0.30, interpolation=cv.INTER_NEAREST)
    # resizedOriginalFPImg = cv.resize(originalFPImg, (0,0), fx=0.30, fy=0.30, interpolation=cv.INTER_NEAREST)

    # get dimensions of the input image
    rows, cols = img.shape

    # initialize
    # create a node (object of the Node class) for each pixel in the image
    nodes = []
    for x in range(rows):
        for y in range(cols):
            newNode = Node([x,y])
            nodes.append(newNode)

    # set start node, goal node
    print("Click anywhere to set the goal position.")
    goal = setPosWithMouse(originalFPImg, 'Civilian')
    try:
        # for FP 4 use goal = 175, 72
        img[goal[0], goal[1]]
    except IndexError:
        print("Goal node is out of image bounds! Setting default goal position...")
        goal = [rows-1, cols-1]
    # if the goal node is not traversable, then exit
    if not findNodeHavingCoords(goal).isTraversable():
        print("Goal node is not traversable!")
        raise SystemExit

    print("Click anywhere to set the start position.")
    start = setPosWithMouse(originalFPImg, 'Rescue Team')      
    try:
        img[start[0], start[1]]
    except IndexError:
        print("Start node is out of image bounds! Setting default start position [0,0]...")
        start = [0,0]

    open = []
    closed = []
    # add the start node to OPEN
    startNode = findNodeHavingCoords(start)
    open.append(startNode)
    startNode.setParent(startNode) # set the start node's parent to itself
    startNode.gCost = 0

    pathFound = False
    # core loop
    startTime = time.time()
    print("\nFinding path, please wait...")
    for i in range(15000): # just a hard limit for safety
        # set current to the node in OPEN with the lowest fCost. Here, sorted() will sort by fCost because __lt__ was manually defined to do so.
        try:
            current = sorted(open)[0]
        except IndexError:
            print("A path could not be found.")
            raise SystemExit
        # remove current from open
        open.remove(current)
        # add current to closed
        closed.append(current)

        # if current is the goal node, then the path has been found
        if current.coords == goal:
            pathFound = True
            break

        #calculate neighbors list (of current)
        neighbors = getNeighbors(current)
        
        # for each neighbor of the current node...
        for neighbor in neighbors:
            # if neighbor is not traversable or neighbor is in CLOSED
            if not neighbor.isTraversable() or neighbor in closed:
                continue # skip to the next neighbor

            # if neighbor is not in OPEN || new path to neighbor is shorter
            if neighbor not in open or isNewPathShorter(neighbor, current):
                # set parent of neighbor to current
                neighbor.setParent(current)
                
                # set fCost of neighbor
                neighbor.calcFCost()

                # if neighbor is not in OPEN
                if neighbor not in open:
                    open.append(neighbor) # add neighbor to open
    else: # runs if the for loop exits without touching a break statement
        print("ERROR: A path could not be found!")
        goal = current.coords
        # raise SystemExit # terminate the code early

    # if the program hasn't terminated, then the path has surely been found.
    if pathFound: print('Path found.')
    endTime = time.time()
    print(f'Elapsed time: {endTime - startTime:.2f} seconds.')
    print("\nDrawing path...")
    pathNodes = getPath(goal)
    newImg = drawPath(pathNodes, img)
    finalImg = overlayPath(newImg, originalFPImg)
    print("Done.")

    # save test output image
    cv.imwrite('Modules/3_Pathfinding/TestOutput.png', finalImg)
    cv.imshow('Output', finalImg)
    cv.waitKey(0)
    cv.destroyAllWindows
if __name__ == '__main__':
    main()

# Module function
def calculatePath(goal, start, locIndex):
    '''Takes 2 integer arrays and a string as input. This function calculates the shortest path
    between start and goal positions in the floorplan specified by locIndex. The output image is
    written into the static folder.'''

    class Node:
        '''Each object of this class represents a pixel.'''

        def __init__(self, coords):
            '''coords is a list of the form [x,y]'''

            self.coords = coords
            self.xCoord = self.coords[0]
            self.yCoord = self.coords[1]
            self.pixelColor = img[self.xCoord, self.yCoord]
            self.fCost = 1000000
        
        def __str__(self):
            return ','.join(str(x) for x in self.coords)

        def __lt__(self, other):
            '''Allows the sorted() function to sort nodes by fCost'''

            return self.fCost < other.fCost
        
        def isTraversable(self):
            '''Returns True if the pixel corresponding to the node is white'''

            if self.pixelColor == 255: return True
            else: return False

        def setParent(self, parent):
            self.parent = parent

        def calcAdjacencyTo(self, tgtNode):
            '''Returns 'x' if the node is diagonally adjacent to the target node, else returns '+' '''

            xCoord = self.xCoord
            yCoord = self.yCoord
            node = tgtNode
            if node.xCoord == xCoord-1 and node.yCoord == yCoord: # top
                return '+'
            if node.xCoord == xCoord-1 and node.yCoord == yCoord+1: # top right
                return 'x'
            if node.xCoord == xCoord and node.yCoord == yCoord+1: # right
                return '+'
            if node.xCoord == xCoord+1 and node.yCoord == yCoord+1: # bottom right
                return 'x'
            if node.xCoord == xCoord+1 and node.yCoord == yCoord: # bottom
                return '+'
            if node.xCoord == xCoord+1 and node.yCoord == yCoord-1: # bottom left
                return 'x'
            if node.xCoord == xCoord and node.yCoord == yCoord-1: # left
                return '+'
            if node.xCoord == xCoord-1 and node.yCoord == yCoord-1: # top left
                return 'x'


        def calcGCost(self):
            '''Sets the node's gCost, which is the distance from the start node.'''

            adj = self.calcAdjacencyTo(self.parent)
            if adj == '+':
                self.gCost = 10 + self.parent.gCost
            if adj == 'x':
                self.gCost = 14 + self.parent.gCost

        def calcHCost(self):
            '''Sets the node's hCost, which is the distance to the goal node.'''

            xCoord = self.xCoord
            yCoord = self.yCoord
            goalNode = findNodeHavingCoords(goal) # sets goal node
            x = abs(goalNode.xCoord - xCoord)
            y = abs(goalNode.yCoord - yCoord)
            if x<y: # x is smaller than y
                self.hCost = 14*x + 10*(y-x)
            else: # y is smaller than x
                self.hCost = 14*y + 10*(x-y)


        def calcFCost(self):
            '''Sets the nodes fCost.
                fCost = gCost + hCost'''

            self.calcGCost()
            self.calcHCost()
            self.fCost = self.gCost + self.hCost


    def findNodeHavingCoords(coords):
        '''Returns the node in the list "nodes" which has the coordinates "coords." '''

        x = coords[0]
        y = coords[1]
        oneD = (x * cols) + y
        return nodes[oneD]

    def getNeighbors(centerNode):
        '''Returns a list of adjacent nodes of the input node'''
        # neighbors = []
        # xCoord = centerNode.xCoord
        # yCoord = centerNode.yCoord
        # for node in nodes:
        #     if node.xCoord == xCoord-1 and node.yCoord == yCoord: # top
        #         neighbors.append(node)
        #     if node.xCoord == xCoord-1 and node.yCoord == yCoord+1: # top right
        #         neighbors.append(node)
        #     if node.xCoord == xCoord and node.yCoord == yCoord+1: # right
        #         neighbors.append(node)
        #     if node.xCoord == xCoord+1 and node.yCoord == yCoord+1: # bottom right
        #         neighbors.append(node)
        #     if node.xCoord == xCoord+1 and node.yCoord == yCoord: # bottom
        #         neighbors.append(node)
        #     if node.xCoord == xCoord+1 and node.yCoord == yCoord-1: # bottom left
        #         neighbors.append(node)
        #     if node.xCoord == xCoord and node.yCoord == yCoord-1: # left
        #         neighbors.append(node)
        #     if node.xCoord == xCoord-1 and node.yCoord == yCoord-1: # top left
        #         neighbors.append(node)
        # return neighbors

        neighbors = []
        x = centerNode.xCoord
        y = centerNode.yCoord
        try:
            if x-1<0: raise IndexError
            coords = [x-1, y]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            if x-1<0: raise IndexError
            temp = img[x-1, y+1]
            coords = [x-1, y+1]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            temp = img[x, y+1]
            coords = [x, y+1]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            temp = img[x+1, y+1]
            coords = [x+1, y+1]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            temp = img[x+1, y]
            coords = [x+1, y]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            if y-1<0: raise IndexError
            temp = img[x+1, y-1]
            coords = [x+1, y-1]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            if y-1<0: raise IndexError
            temp = img[x, y-1]
            coords = [x, y-1]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass
        try:
            if y-1<0 or x-1<0: raise IndexError
            temp = img[x-1, y-1]
            coords = [x-1, y-1]
            neighbors.append(findNodeHavingCoords(coords))
        except IndexError: pass

        return neighbors

    def isNewPathShorter(node, current):
        '''Returns True if the node's gCost to "current" is less than its gCost'''

        if node not in open:
            return False
        oldGCost = node.gCost
        adj = node.calcAdjacencyTo(current)
        if adj == '+':
                newGCost = 10 + current.gCost
        if adj == 'x':
                newGCost = 14 + current.gCost
        if newGCost < oldGCost:
            return True

    def getPath(coords):
        '''Returns a list with all nodes on the path.
        The path is from the node with coordinates "coords" to the start node.'''
        pathNodes = []
        node = findNodeHavingCoords(coords)
        while(node.parent != node):
            pathNodes.append(node)
            node = node.parent
        pathNodes.append(node)
        return pathNodes

    def drawPath(pathNodes, img):
        '''Draws a path on the input image and returns the resulting image.
        All pixels that correspond to the nodes in the input list will be colored red.
        '''
        img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        # for x in range(rows):
        #     for y in range(cols):

        #         for node in nodes:
        #             if node.coords == [x,y]:
        #                 # color that pixel red
        #                 img[x,y] = [0,0,255]
        for node in pathNodes:
            img[node.xCoord, node.yCoord] = [0,0,255]
        img[pathNodes[0].xCoord, pathNodes[0].yCoord] = [0, 255, 0]
        return img

    def overlayPath(img, fp):
        
        # scale new image to match ogFPImg
        shapeIWant = []
        shapeIWant.append(fp.shape[1])
        shapeIWant.append(fp.shape[0])
        shapeIWant = tuple(shapeIWant)
        img = cv.resize(img, shapeIWant, interpolation=cv.INTER_NEAREST)

        # fp = cv.addWeighted(img, .3, fp, .7, 0)
        # return fp

        for x in range(ogRows):
            for y in range(ogCols):
                
                if (img[x,y] == [0,0,255]).all(): #if pixel is red
                    fp[x,y] = [0,0,255]
                if (img[x,y] == [0,255,0]).all(): #if pixel is green
                    fp[x,y] = [0,255,0]
        return fp

    def onMouse(event, x, y, flags, param):
        global mousePos
        if event == cv.EVENT_LBUTTONDOWN:
            x, y = y, x
            mousePos = [x,y]
            cv.destroyWindow(globalLabel)
            # print(f'{mousePos}\tPress any key to confirm...')

    def setPosWithMouse(img, label):
        '''Returns the position of the cursor when LeftButton is pressed.'''
        
        global globalLabel
        globalLabel = f'Set {label}\'s position'
        cv.imshow(f'Set {label}\'s position', img)
        cv.setMouseCallback(f'Set {label}\'s position', onMouse)
        cv.waitKey(0)
        # cv.destroyWindow(f'Set {label}\'s position')
        try:
            mousePos[0] = round(mousePos[0]*0.3)
            mousePos[1] = round(mousePos[1]*0.3)
        except NameError:
            print("Failed to set position, exiting...")
            raise SystemExit
        return mousePos

    # read testFP in grayscale mode #FIXME: Comments are out of date.
    originalFPImg = cv.imread(f'static/floor-plans/{locIndex}.jpg')
    ogRows = originalFPImg.shape[0]
    ogCols = originalFPImg.shape[1]
    inputImg = cv.imread('static/floor-plans/processed.png', cv.IMREAD_GRAYSCALE)
    inputImg = cv.bitwise_not(inputImg) # inverted original image
    img = cv.resize(inputImg, (0,0), fx=0.30, fy=0.30, interpolation=cv.INTER_NEAREST)
    # resizedOriginalFPImg = cv.resize(originalFPImg, (0,0), fx=0.30, fy=0.30, interpolation=cv.INTER_NEAREST)

    # scale down goal and start values (multiply by 0.30)
    goal[0] = round(goal[0]*0.30)
    goal[1] = round(goal[1]*0.30)
    start[0] = round(start[0]*0.30)
    start[1] = round(start[1]*0.30)

    # get dimensions of the input image
    rows, cols = img.shape

    # initialize
    # create a node (object of the Node class) for each pixel in the image
    nodes = []
    for x in range(rows):
        for y in range(cols):
            newNode = Node([x,y])
            nodes.append(newNode)

    # set start node, goal node
    print("Click anywhere to set the goal position.")
    # goal = setPosWithMouse(originalFPImg, 'Civilian')
    try:
        # for FP 4 use goal = 175, 72
        img[goal[0], goal[1]]
    except IndexError:
        print("Goal node is out of image bounds! Setting default goal position...")
        print(goal)
        goal = [rows-1, cols-1]
    # if the goal node is not traversable, then exit
    if not findNodeHavingCoords(goal).isTraversable():
        print("Goal node is not traversable!")
        raise SystemExit

    print("Click anywhere to set the start position.")
    # start = setPosWithMouse(originalFPImg, 'Rescue Team')      
    try:
        img[start[0], start[1]]
    except IndexError:
        print("Start node is out of image bounds! Setting default start position [0,0]...")
        print(start)
        start = [0,0]

    open = []
    closed = []
    # add the start node to OPEN
    startNode = findNodeHavingCoords(start)
    open.append(startNode)
    startNode.setParent(startNode) # set the start node's parent to itself
    startNode.gCost = 0

    pathFound = False
    # core loop
    startTime = time.time()
    print("\nFinding path, please wait...")
    for i in range(15000): # just a hard limit for safety
        # set current to the node in OPEN with the lowest fCost. Here, sorted() will sort by fCost because __lt__ was manually defined to do so.
        try:
            current = sorted(open)[0]
        except IndexError:
            print("A path could not be found.")
            raise SystemExit
        # remove current from open
        open.remove(current)
        # add current to closed
        closed.append(current)

        # if current is the goal node, then the path has been found
        if current.coords == goal:
            pathFound = True
            break

        #calculate neighbors list (of current)
        neighbors = getNeighbors(current)
        
        # for each neighbor of the current node...
        for neighbor in neighbors:
            # if neighbor is not traversable or neighbor is in CLOSED
            if not neighbor.isTraversable() or neighbor in closed:
                continue # skip to the next neighbor

            # if neighbor is not in OPEN || new path to neighbor is shorter
            if neighbor not in open or isNewPathShorter(neighbor, current):
                # set parent of neighbor to current
                neighbor.setParent(current)
                
                # set fCost of neighbor
                neighbor.calcFCost()

                # if neighbor is not in OPEN
                if neighbor not in open:
                    open.append(neighbor) # add neighbor to open
    else: # runs if the for loop exits without touching a break statement
        print("ERROR: A path could not be found!")
        goal = current.coords
        # raise SystemExit # terminate the code early

    # if the program hasn't terminated, then the path has surely been found.
    if pathFound: print('Path found.')
    endTime = time.time()
    print(f'Elapsed time: {endTime - startTime:.2f} seconds.')
    print("\nDrawing path...")
    pathNodes = getPath(goal)
    newImg = drawPath(pathNodes, img)
    finalImg = overlayPath(newImg, originalFPImg)
    print("Done.")

    # save test output image
    cv.imwrite('static/floor-plans/path.png', finalImg)
    # cv.imshow('Output', finalImg)
    # cv.waitKey(0)
    # cv.destroyAllWindows