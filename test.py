
import numpy as np
import math

class point:
    def __init__(self,x,y):
        self.x = x
        self.y = y 
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
        b = (self.x - pGoal.x)**2 + (self.y - pGoal.y)**2
        return math.sqrt(b)

def isSame(p1, p2):
    if (p1.x == p2.x and p1.y == p2.y):
        return True
    
    return False

def inBoard(x,y):
    return (y >= 0 and y < map.shape[0] 
                and x >= 0 and x < map.shape[1]) 

def gDistance(p1, pDest):
    return math.sqrt((p1.x-pDest.x)**2 + (p1.y-pDest.y)**2)

class Frontier:
    def __init__(self):
        self.list = []

    def append(self,p):

        # list dang rong~
        if (not self.list):
            self.list.append(p)
            return
        
        # neu p la min 
        if (p < self.list[-1]):
            self.list.append(p)
            return


        i = len(self.list)-1
        self.list.append(self.list[-1])
        
        while (i >= 0 and p > self.list[i]):
            i -= 1

        # ktra TH total = nhau tai day
        if (p == self.list[i]):
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



map =np.array( [[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1]] )

goal = point(5,5)
print(map)

f =Frontier()
f.append(3)
f.append(3)
f.append(9)
f.append(5)
f.append(7)
f.append(5)
f.append(1)
f.append(2)

print(f.list)
