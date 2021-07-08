from PIL import Image
import numpy as np
import math as m

def toMatrix(imagePath):
    img = Image.open(imagePath)
    width, height = img.size
    print()
    rgba = list(img.getdata())

    data = []
    temp = []

    count = 0
    for row in range(height):
        for col in range(width):
            temp.append(rgba[count][0])
            count += 1

        data.append(temp)
        temp = []

    return data

def sgn(x):
    if (x < 0):
        return -1
    elif (x > 0):
        return 1
    else:
        return 0

class point:
    def __init__(self,x,y):
        self.x = x
        self.y = y 
        self.a = globalMap[x,y]

def gDistance(p1, pDest):
    if (p1.a > pDest.a):
        return m.sqrt((p1.x-pDest.x)**2 + (p1.y-pDest.y)**2) + 0.5*(p1.a-pDest.a)
    else:
        return m.sqrt((p1.x-pDest.x)**2 + (p1.y-pDest.y)**2) + 1.5*(pDest.a-p1.a) 

data = toMatrix('ff.bmp')
globalMap = np.array(data)

print(globalMap[0][0], globalMap[0][1])
print(gDistance(point(0,0), point(0,1)))