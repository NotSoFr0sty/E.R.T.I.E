import sys
import os
sys.path.append(os.path.abspath("Modules"))
import cv2 as cv
from One_ImageProcessing.ImageProcessing import processFloorPlan
from Two_2Dto3D.my2Dto3D import convertTo3D
from Three_Pathfinding.v1 import calculatePath

# # Test Mod1 and Mod2
# def main():
#     processedImg = processFloorPlan('Floorplans/4.jpg')
#     cv.imshow('Output', processedImg)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#     convertTo3D(processedImg)    

# Test Mod3 Pathfinding
def main():
    
    goal = [1, 1]
    start = [1, 20]
    locIndex = "2"
    calculatePath(goal, start, locIndex)

if __name__ == '__main__':
    main()
