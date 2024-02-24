'''Module 2 - 2D to 3D Conversion
Algorithm:
Read processed floor plan and get its dimensions
Set faceCount = total_no_of_pixels_of_floor_plan * 2
Initialize a numpy zeros array, called data, with shape = faceCount
Read the floor plan pixel by pixel
Create 2 faces for each pixel (each face is made up of exactly 3 vertices)
If the pixel is white, then set the faces’ Z values to wallHeight
Else set Z values to the default, 0
Create the 3D mesh using mesh.Mesh(data)
Save the mesh as an STL model
'''

import numpy
from stl import mesh
import cv2 as cv

# read floor plan in grayscale mode
img = cv.imread('Floorplans/TestFP.png', cv.IMREAD_GRAYSCALE)
# cv.imshow('2D Input Floor Plan', img)
# cv.waitKey(0)
# cv.destroyAllWindows()

# get dimensions of the input image
rows, cols = img.shape
pixelCount = rows*cols

# initialize 3D variables
faceCount = pixelCount * 2
wallHeight = 10
data = numpy.zeros(faceCount, dtype=mesh.Mesh.dtype)

# read floor plan pixel by pixel and create faces (2 faces per pixel, each face is a triangle)
i = 0
for x in range(rows):
    for y in range(cols):
        # if pixel is white, then all vertices are at wallHeight (for the z value)
        if img[x,y] == 255:
            z = wallHeight
            data['vectors'][i] = numpy.array([[x, y, z],
                                            [x, y+1, z],
                                            [x+1, y, z]])
            i+=1
            data['vectors'][i] = numpy.array([[x, y+1, z],
                                            [x+1, y+1, z],
                                            [x+1, y, z]])
            i+=1
            continue
        # else the pixel is black AND the z values for each vertice must be set according to the adjacent pixels
        zTL = zTR = zBL = zBR = 0    
        
        # determine z value of the top-left vertice (zTL)
        # MAKE SURE X AND Y ARE GREATER THAN OR EQUAL TO ZERO BECAUSE NEGATIVE INDEX MEANS FROM THE REAR!!!
        try:
            temp = img[3, 3]
            print(temp)
        except IndexError:
            print("indexError found")
        try:
            temp = img[x-1,y-1]
            if img[x-1,y-1] == 255:
                zTL = wallHeight
        except IndexError:
            print("indexError found")
        try:
            if img[x-1,y] == 255:
                zTL = wallHeight
        except IndexError:
            print("indexError found")
        try:
            if img[x,y-1] == 255:
                zTL = wallHeight
        except IndexError:
            print("indexError found")


# create the 3D mesh
# testMesh = mesh.Mesh(data)
# testMesh.save('STL Models/Test2.stl')



