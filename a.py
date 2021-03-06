from PIL import Image
import numpy as np
import math

MAX = 99999

# convert image to matrix
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
        self.cost = MAX
        self.total = MAX
        self.parent = None

    def canClimb(self, p):
        if (abs(self.a - p.a) > globalM):
            return False

        return True

    # accessible point
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

    def h(self, pGoal, i):
        
        b = (self.x - pGoal.x)**2 + (self.y - pGoal.y)**2
        if (i == 1):    
            a = (self.a - pGoal.a)**2
            return math.sqrt(a+b)
        if (i==2):
            return math.sqrt(b)
        if (i==3):
            a = abs(self.a - pGoal.a)
            return math.sqrt(b) + a
        if (i==4):
            return 0
            
        

def isSame(p1, p2):
    
    if (p1.x == p2.x and p1.y == p2.y):
        return True
    
    return False

# check a point is still in board
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
    def __init__(self, i):
        self.list = []
        self.store = globalMap.copy()
        self.store.fill(MAX)
        self.count = 0
        self.hType = i

    def updateCost(self,p):
        if (p.parent == None):
            p.cost = 0
            p.total = 0
        else:
            p.cost = p.parent.cost + gDistance(p.parent,p)
            p.total = p.cost + p.h(globalG,self.hType)

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
            while (i > 0 and p.total == self.list[i-1].total 
                and p.h(globalG,self.hType) > self.list[i-1].h(globalG,self.hType)):
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
        if (len(self.list) == 0):
            return None
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

def drawPath(img, pG,i):
    #img = Image.open(filePath)
    curP = pG 
    while (curP.parent != None):
        img.putpixel((curP.x,curP.y), (255,0,0))
        curP = curP.parent

    img.putpixel((curP.x,curP.y), (255,0,0))
    output=filePath.replace(".bmp",str(i)+".bmp")
    img.save(output)

def ref(i):
    d = math.sqrt((start.x-globalG.x)**2 + (start.y-globalG.y)**2)
    
    if (i != 3):
        return d + 15

    return d + abs(start.a - globalG.a)

def findAStart(filePath,i):
    img = Image.open(filePath) 

    f = pointFrontier(i)
    
    # push Start point to frontier
    f.updateCost(start)
    f.append(start)
    curP = f.pop()

    reference = ref(i)
    val= globalMap.shape[0]*globalMap.shape[1]

    while ((not isSame(curP, globalG)) and f.count < val):
        for p in curP.adjList():
            if (curP.canClimb(p)):
                p.parent = curP 
                if (f.updateCost(p) and p.h(globalG,f.hType) < reference):
                    f.append(p)
                    #img.putpixel((curP.x,curP.y), (0,255,0))

        # print(f.store[210:225,69:82], end='\n\n')
        # print("frontier: ")
        # for item in f.list:
        #     print(item.x, item.y,sep=',', end=' ')
        #     print(int(item.total), end=' ')
        #print()
        curP = f.pop()
        if (curP == None):
            print("points: ", f.count)
            print("No way")
            return
        #print("pop:" , end=" ")
        #curP.display()

    #print(f.store)
    WriteFile(f.count,curP.cost,i)
    print("heuristic ",i)
    print("points: ", f.count)
    print("cost:", curP.cost)

    drawPath(img,curP,i)
    
def Readfile(file):
    input= open(file,"r")
    res=[]
    
    for i in input:
        res.append(i)
    
    for i in range(2):
        a1= res[i].index("(")
        a2=res[i].index(";")
        a3=res[i].index(")")
        x=int(res[i][a1+1:a2])
        y=int(res[i][a2+1:a3])
        point=[x,y]
        res[i]=point
    
    res[2]=int(res[2])
    return res

def WriteFile(points,cost,i):
    OutputTextFile=InputTextFile.replace("input","output"+str(i))
    output= open(OutputTextFile,"w")
    output.write(str(cost)+"\n")
    output.write(str(points))


#--------------------main---------------------
InputTextFile = "input.txt"


res=Readfile(InputTextFile)

filePath = "map.bmp"
data = toMatrix(filePath)
globalMap = np.array(data)
globalM=res[2]
globalG = point(res[1][0],res[1][1])

start = point(res[0][0],res[0][1])

print(globalMap.shape[1], globalMap.shape[0])



for i in range(1,5):
    findAStart(filePath, i)




