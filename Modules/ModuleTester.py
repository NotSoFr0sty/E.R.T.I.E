import sys
import os
sys.path.append(os.path.abspath("Modules"))
import cv2 as cv
from One_ImageProcessing.ImageProcessing import processFloorPlan
from Two_2Dto3D.my2Dto3D import convertTo3D

# Test Mod1 and Mod2
def main():
    processedImg = processFloorPlan('Floorplans/4.jpg')
    cv.imshow('Output', processedImg)
    cv.waitKey(0)
    cv.destroyAllWindows()
    convertTo3D(processedImg)    

if __name__ == '__main__':
    main()
