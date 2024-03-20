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

    def calcAdjacencyToParent(self):
        '''Returns 'x' if the node is diagonally adjacent to its parent, else returns '+' '''

        xCoord = self.xCoord
        yCoord = self.yCoord
        node = self.parent
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
        '''Sets the gCost of the node.
            A node's gCost is its distance from the start node.'''

        adj = self.calcAdjacencyToParent()
        if adj == '+':
            self.gCost = 10 + self.parent.gCost
        if adj == 'x':
            self.gCost = 14 + self.parent.gCost

    def calcHCost(self):
        '''Sets the nodes '''

        xCoord = self.xCoord
        yCoord = self.yCoord
        #TODO: complete this before all other TODOs!!!

    def calcFCost(self):
        '''Sets the nodes fCost.
            fCost = gCost + hCost'''

        self.calcGCost()
        self.calcHCost()
        self.fCost = self.gCost + self.hCost


def findNodeHavingCoords(coords):
    '''Returns the node in the list "nodes" which has the coordinates "coords." '''

    for node in nodes:
        if node.coords == coords:
            return node

def getNeighbors(centerNode):
    '''Returns a list of adjacent nodes of the input node'''

    neighbors = []
    xCoord = centerNode.xCoord
    yCoord = centerNode.yCoord
    for node in nodes:
        if node.xCoord == xCoord-1 and node.yCoord == yCoord: # top
            neighbors.append(node)
        if node.xCoord == xCoord-1 and node.yCoord == yCoord+1: # top right
            neighbors.append(node)
        if node.xCoord == xCoord and node.yCoord == yCoord+1: # right
            neighbors.append(node)
        if node.xCoord == xCoord+1 and node.yCoord == yCoord+1: # bottom right
            neighbors.append(node)
        if node.xCoord == xCoord+1 and node.yCoord == yCoord: # bottom
            neighbors.append(node)
        if node.xCoord == xCoord+1 and node.yCoord == yCoord-1: # bottom left
            neighbors.append(node)
        if node.xCoord == xCoord and node.yCoord == yCoord-1: # left
            neighbors.append(node)
        if node.xCoord == xCoord-1 and node.yCoord == yCoord-1: # top left
            neighbors.append(node)
    
    return neighbors


# read testFP in grayscale mode
img = cv.imread('Floorplans/testFP.png', cv.IMREAD_GRAYSCALE)

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
start = [0,0]
goal = [rows-1, cols-1]
open = []
closed = []
# add the start node to OPEN
startNode = findNodeHavingCoords(start)
open.append(startNode)
startNode.setParent(startNode) # set the start node's parent to itself
startNode.gCost = 0
# set goal node
goalNode = findNodeHavingCoords(goal)

pathFound = False
# core loop
for i in range(1): #TODO: set the proper range/condition
    # set current to the node in OPEN with the lowest fCost. Here, sorted() will sort by fCost because __lt__ was manually defined to do so.
    current = sorted(open)[0]
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
        if neighbor not in open or isNewPathShorter(neighbor): #TODO: define this function
            # set parent of neighbor to current
            neighbor.setParent(current)
            
            # set fCost of neighbor
            neighbor.calcFCost()

            # if neighbor is not in OPEN
            if neighbor not in open:
                open.append(neighbor) # add neighbor to open
else: print("ERROR: Path not found!")

# save test output image
cv.imwrite('Modules/3_Pathfinding/testOutput.png', img)