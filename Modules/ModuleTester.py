import sys
import os
sys.path.append(os.path.abspath("Modules/1_ImageProcessing"))
import cv2 as cv
from ImageProcessing import processFloorPlan

# Test Mod1
def main():
    img = processFloorPlan('Floorplans/4.jpg')
    cv.imshow('Output', img)
    cv.waitKey(0)
    cv.destroyAllWindows()    

if __name__ == '__main__':
    main()
