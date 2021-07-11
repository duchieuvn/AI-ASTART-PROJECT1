from PIL import Image
import numpy as np
import math

MAX = 999

def toMatrix(imagePath):
    img = Image.open(imagePath)
    width, height = img.size
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
        #return math.sqrt(b)

def isSame(p1, p2):
    if (p1.x == p2.x and p1.y == p2.y):
        return True
    
    return False

def inBoard(x,y):
    return (y >= 0 and y < globalMap.shape[0] 
                and x >= 0 and x < globalMap.shape[1]) 

def gDistance(p1, pDest):

    d = math.sqrt((p1.x-pDest.x)**2 + (p1.y-pDest.y)**2)

    if (p1.a > pDest.a):
        return d + 0.5*(p1.a-pDest.a)
    else:
        return d + 1.5*(pDest.a-p1.a) 

class pointFrontier:
    def __init__(self):
        self.list = []
        self.store = globalMap.copy()
        self.store.fill(MAX)
        self.count = 0

    def updateCost(self,p):
        if (p.parent == None):
            p.cost = 0
            p.total = 0
        else:
            p.cost = p.parent.cost + gDistance(p.parent,p)
            p.total = p.cost + p.h1(globalG)

        if (p.total < self.store[p.y,p.x]):
            if (self.store[p.y,p.x] == MAX):
                self.count += 1

            self.store[p.y,p.x] = p.total
            return True
        
        return False

    def append(self,p):
        
        # list dang rong~
        if (not self.list):
            self.list.append(p)
            return
        

        # neu p la min 
        if (p.h1(globalG) < self.list[-1].h1(globalG)):
            self.list.append(p)
            return

        
        i = len(self.list)-1
        self.list.append(self.list[-1])
        
        while (i >= 0 and p.h1(globalG) > self.list[i].h1(globalG)):
            i -= 1

        # ktra TH total = nhau tai day
        if (p.h1(globalG) == self.list[i].h1(globalG)):
            i += 1
            while (i > 0 and p.h1(globalG) == self.list[i-1].h1(globalG) 
                and p.total > self.list[i-1].total):
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


def tracePath(pG):
    print("total cost: ", pG.cost)
    curP = pG
    Path = []
    while (curP.parent != None):
        print(curP.x,curP.y,sep=',', end=' -> ')
        Path.append(curP)
        curP = curP.parent
    
    print(curP.x,curP.y,sep=',')
    Path.append(curP)

    return Path

def drawPath(img, pG):
    #img = Image.open(filePath)
    curP = pG 
    while (curP.parent != None):
        img.putpixel((curP.x,curP.y), (255,0,0))
        curP = curP.parent

    img.putpixel((curP.x,curP.y), (255,0,0))
    img.save("out.bmp")

def findAStart(filePath):
    img = Image.open(filePath) 

    f = pointFrontier()
    
    # push Start point to frontier
    f.updateCost(start)
    f.append(start)
    curP = f.pop()

    reference = gDistance(start,globalG)

    while ((not isSame(curP, globalG)) and f.count < 90000):
        for p in curP.adjList():
            if (curP.canClimb(p)):
                p.parent = curP 
                if (f.updateCost(p) and p.h1(globalG) < reference):
                    #print("push (",p.x,p.y,")" )
                    f.append(p)
                    img.putpixel((curP.x,curP.y), (0,255,0))
                    # print("count:", f.count)

        print(f.store[210:225,69:82], end='\n\n')
        print("frontier: ")
        for item in f.list:
            #print(item.x, item.y,sep=',', end=' ')
            print(int(item.total), end=' ')
        print()
        curP = f.pop()
        #print("pop:" , end=" ")
        #curP.display()

    #print(f.store)

    print("points: ", f.count)
    print("cost:", curP.cost)

    drawPath(img,curP)
    


#--------------------main---------------------

filePath = "map.bmp"
data = toMatrix(filePath)
globalMap = np.array(data)
globalM = 10
globalG = point(96,311)

start = point(74,213)

print(globalMap.shape[1], globalMap.shape[0])

findAStart(filePath)




