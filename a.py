
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

    def adjList(self):
        k = [[0,1],[0,-1],[1,0],[-1,0],
                [1,1],[1,-1],[-1,1],[-1,-1]]
        pL = []
        for move in k:
            if inBoard(self.x+move[0], self.y+move[1]):
                pL.append( point(self.x+move[0], self.y+move[1]) )

        return pL


    def h1(self, pGoal):
        a = (self.a - pGoal.a)**2
        b = (self.x - pGoal.x)**2 + (self.y - pGoal.y)**2
        return math.sqrt(a + b)

def inBoard(x,y):
    return (y >= 0 and y < globalMap.shape[0] 
                and x >= 0 and x < globalMap.shape[1]) 

def gDistance(p1, pDest):
    if (p1.a > pDest.a):
        return math.sqrt((p1.x-pDest.x)**2 + (p1.y-pDest.y)**2) + 0.5*(p1.a-pDest.a)
    else:
        return math.sqrt((p1.x-pDest.x)**2 + (p1.y-pDest.y)**2) + 1.5*(pDest.a-p1.a) 

class pointFrontier:
    def __init__(self):
        self.list = []

    def append(self,p, curCost):


        if (not self.list):
            self.list.append(p)
            return
        
        #calculate A* cost, total = A* cost
        p.total = curCost + gDistance(p.parent, p) + p.h1(globalG)
        
        if (p.total < self.list[-1].total):
            self.list.append(p)
            return

        i = len(self.list)
        self.list.append(self.list[-1])
        
        while (i >= 0 and p.total > self.list[i].total):
            i -= 1

        # ktra TH total = nhau tai day

        for j in range(len(self.list)-2, i, -1):
            self.list[j] = self.list[j-1]

        # add p to frontier
        self.list[i+1] = p

    def pop(self):
        return self.list.pop()


def findAStart():
    
    f = pointFrontier()
    # push Start point to frontier
    f.append(point(3, 2), 0)
    curDistance = 0
    curP = point(3, 2)
    count = 0
    while (curP.x != globalG.x and curP.y != globalG.y and count < 200):
        for p in curP.adjList():
            if (curP.canClimb(p)):
                p.parent = curP 
                f.append(p, curDistance)
                count += 1
        
        curP = f.pop()
        curDistance += gDistance(curP.parent, curP)

    print("points: ", count)


#--------------------main---------------------

data = toMatrix('ff.bmp')
globalMap = np.array(data)
globalM = 10
globalG = point(8,8)

print(globalMap[:10,:10])

findAStart()
