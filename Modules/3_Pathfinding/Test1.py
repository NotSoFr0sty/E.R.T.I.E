'''
A* Pathfinding Algorithm:

OPEN //set of nodes to be evaluated
CLOSED //set of nodes already evaluated (potential path)
add the start node to OPEN

loop
    current = node in OPEN with the lowest f_cost
    remove current from OPEN
    add current to CLOSED

    if current is the goal node //path has been found
        return
    
    for each neighbor of the current node
        if neighbor is not traversable or neighbor is in CLOSED
            skip to next neighbor
        
        if neighbor is not in OPEN || new path to neighbor is shorter
            set f_cost of neighbor
            set parent of neighbor to current
            if neighbor is not in OPEN
                add neighbor to OPEN
'''
'''
For Test1.py
Open the testFP
Start node is topLeft (top-most, left-most) pixel
Goal node is bottomRight pixel
NOTE: Black means wall, white means floor
'''

import cv2 as cv
import numpy as np

class Node:
    '''Each object of this class represents a pixel.'''

    def __init__(self, coords):
        '''coords is a list of the form [x,y]'''

        self.coords = coords

# read testFP in grayscale mode
img = cv.imread('Floorplans/testFP.png', cv.IMREAD_GRAYSCALE)

# get dimensions of the input image
rows, cols = img.shape

# initialize
# create an object for each pixel in the image
nodes = []
for x in range(rows):
    for y in range(cols):
        newNode = Node([x,y])
        nodes.append(newNode)
#         
start = [0,0]
goal = [rows-1, cols-1]
open = []
closed = []
# add the start node to OPEN
for node in nodes:
    if node.coords == start:
        open.append(node)




# save test output image
cv.imwrite('Modules/3_Pathfinding/testOutput.png', img)