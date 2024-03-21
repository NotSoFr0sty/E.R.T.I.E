import numpy as np
import cv2 as cv

# myArray = np.array([[1,2,3],
#                     [4,5,6],
#                     [7,8,9]])
# print(myArray)
# print(myArray.shape[0])

# i = 0
# for x in range(3):
#     for y in range(3):
#         print(i)
#         i+=1

# img = np.zeros((3,3), dtype = np.int8)
# z = 5
# try:
#     if z>4:
#         raise IndexError
#     temp = img[2,2]
#     print("Inside try block.")
# except IndexError:
#     print("Inside except block.")

# print("After try-except block.")

# class Fruit():
#     def __init__(self, name, price):
#         self.name = name
#         self.price = price

#     # def __lt__(self, other): # other is another instance of Fruit
#     #     return self.price < other.price
    
#     def __gt__(self, other): # other is another instance of Fruit
#         return self.price > other.price

# apple = Fruit("Apple", 5)
# cherry = Fruit("Cherry", 20)
# blueberry = Fruit("Blueberry", 10)
# L = [cherry, apple, blueberry]

# print("-----sorted using comparison operator (without key)-----")
# for f in sorted(L):
#     print(f.name)

def onMouse(event, x, y, flags, param):
    global mousePos
    global img
    if event == cv.EVENT_LBUTTONDOWN:
        mousePos = [x,y]
        print(mousePos)


img = cv.imread('Modules/3_Pathfinding/TestOutput.png')
cv.imshow('image', img)
cv.setMouseCallback('image', onMouse)
cv.waitKey(0)
cv.destroyAllWindows
print(mousePos)
