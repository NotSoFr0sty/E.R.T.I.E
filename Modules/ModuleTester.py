import sys
import os
sys.path.append(os.path.abspath("Modules"))
import cv2 as cv
from ImageProcessing.ImageProcessing import processFloorPlan
# sys.path.append(os.path.abspath("Modules/2_2Dto3D"))
from TwoDto3D.my2Dto3D import convertTo3D

# Test Mod1 and Mod2
def main():
    img = processFloorPlan('Floorplans/4.jpg')
    cv.imshow('Output', img)
    cv.waitKey(0)
    cv.destroyAllWindows()    

if __name__ == '__main__':
    main()
