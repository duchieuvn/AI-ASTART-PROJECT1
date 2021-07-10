
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
        self.a = globalMap[y,x]
        self.cost = 999
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

    def display(self):
        print("(",self.x,",",self.y,")")

    def h1(self, pGoal):
        a = (self.a - pGoal.a)**2
        b = (self.x - pGoal.x)**2 + (self.y - pGoal.y)**2
        return math.sqrt(a+b)

def isSame(p1, p2):
    if (p1.x == p2.x and p1.y == p2.y):
        return True
    
    return False

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

    def append(self,p):
        if (p.parent == None):
            p.cost = 0
            p.total = 0
        else:
            p.cost = p.parent + gDistance(p.parent,p)
            p.total = p.cost + p.h1(globalG)
        
        # list dang rong~
        if (not self.list):
            self.list.append(p)
            return
        

        # neu p la min 
        if (p.total < self.list[-1].total):
            self.list.append(p)
            return

        
        i = len(self.list)-1
        self.list.append(self.list[-1])
        
        while (i >= 0 and p.total > self.list[i].total):
            i -= 1

        # ktra TH total = nhau tai day
        if (p.total == self.list[i].total):
            i += 1
            while (p.total == self.list[i-1].total 
                and p.h1(globalG) > self.list[i-1].h1(globalG)):
                    i -= 1
            
            for j in range(len(self.list)-1, i, -1):
                self.list[j] = self.list[j-1]
            
            self.list[i] = p
            return

        for j in range(len(self.list)-1, i+1, -1):
            self.list[j] = self.list[j-1]

        # add p to frontier
        self.list[i+1] = p

    def pop(self):
        return self.list.pop()


def findAStart():
    b = globalMap.copy()

    f = pointFrontier()
    start = point(1,1)
    # push Start point to frontier
    f.append(start)
    curP = f.pop()
    count = 0
    while ((not isSame(curP, globalG)) and count < 200):
        for p in curP.adjList():
            if (curP.canClimb(p)):
                p.parent = curP 
                f.append(p)
                count += 1
        
        curP = f.pop()
        curP.display()
        b[curP.y,curP.x] = 0

    b[start.y,start.x] = -1
    b[3,4] = -111
    print("points: ", count)
    print(b)
    


#--------------------main---------------------

data = toMatrix('ss.bmp')
d = data[:5][:5]
globalMap = np.array(d)
globalM = 10
globalG = point(4,3)

findAStart()
