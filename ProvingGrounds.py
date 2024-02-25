import numpy as np

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

img = np.zeros((3,3), dtype = np.int8)
z = 5
try:
    temp = img[3,3]
    print("Inside try block.")
except IndexError:
    print("Inside except block.")