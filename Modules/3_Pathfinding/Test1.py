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
'''

import cv2 as cv
import numpy as np

# open testFP
img = cv.imread('Floorplans/testFP.png', cv.IMREAD_GRAYSCALE)


#save test output image
cv.imwrite('Modules/3_Pathfinding/testOutput.png', img)