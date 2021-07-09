
from PIL import Image
import numpy as np
import math

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

class point:
    def __init__(self,x,y):
        self.x = x
        self.y = y 
        self.a = globalMap[x,y]
        self.total = 999
        self.parent = None

    def canClimb(self, p):
        if (abs(self.a - p.a) > globalM):
            return False

        return True

    def h1(self, pGoal):
        a = (self.a - pGoal.a)**2
        b = (self.x - pGoal.x)**2 + (self.y - pGoal.y)**2
        return math.sqrt(a + b)


def gDistance(p1, pDest):
    if (p1.a > pDest.a):
        return math.sqrt((p1.x-pDest.x)**2 + (p1.y-pDest.y)**2) + 0.5*(p1.a-pDest.a)
    else:
        return math.sqrt((p1.x-pDest.x)**2 + (p1.y-pDest.y)**2) + 1.5*(pDest.a-p1.a) 

def costAStart(p, pN):
    return gDistance(p, pN) + pN.h1()

class pointFrontier:
    def __init__(self):
        self.list = []

    def append(self,p, curCost):

        if (not self.list):
            self.list.append(p)
            return

        if (p.a < self.list[-1].a):
            
            self.list.append(p)
            return

        i = len(self.list)
        self.list.append(self.list[-1])
        
        while (i >= 0 and p.a > self.list[i].a):
            i -= 1

        for j in range(len(self.list)-2, i, -1):
            self.list[j] = self.list[j-1]

        # add p to frontier
        self.list[i+1] = p

    def pop(self):
        return self.list.pop()


#--------------------main---------------------

data = toMatrix('ff.bmp')
globalMap = np.array(data)
globalM = 10
globalG = point(70,55)


print("first 10 value of globalMap: ")
print(globalMap[0][:11])

