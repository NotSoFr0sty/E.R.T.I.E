import numpy
import math
from stl import mesh

faceCount = 8
data = numpy.zeros(faceCount, dtype=mesh.Mesh.dtype)
data['vectors'][0] = numpy.array([[0, 0, 1],
                                  [1, 0, 1],
                                  [0, 1, 0]])
data['vectors'][1] = numpy.array([[1, 0, 1],
                                  [0, 1, 0],
                                  [1, 1, 1]])
data['vectors'][2] = numpy.array([[1, 0, 1],
                                  [2, 0, 0],
                                  [1, 1, 1]])
data['vectors'][3] = numpy.array([[2, 0, 0],
                                  [1, 1, 1],
                                  [2, 1, 0]])
data['vectors'][4] = numpy.array([[0, 1, 0],
                                  [1, 1, 1],
                                  [0, 2, 0]])
data['vectors'][5] = numpy.array([[1, 1, 1],
                                  [0, 2, 0],
                                  [1, 2, 0]])
data['vectors'][6] = numpy.array([[1, 1, 1],
                                  [2, 1, 0],
                                  [1, 2, 0]])
data['vectors'][7] = numpy.array([[2, 1, 0],
                                  [1, 2, 0],
                                  [2, 2, 1]])

testMesh = mesh.Mesh(data)
testMesh.save('STL Models/testMesh.stl')