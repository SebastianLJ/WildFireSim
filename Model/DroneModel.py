import numpy as np
import random

class DroneModel():
    VIEWRANGE = 1 #need to ome up with better estimate. 
    MOVERANGE = 2 #7.2 km/h
    
    def __init__(self, n, m, seed, spreadMap, fireMap, droneNumber):
        self.n = n
        self.m = m
        self.seed = seed
        np.random.seed(self.seed)
        random.seed(self.seed)
        self.noisySpreadMap = np.zeros((self.n,self.m), dtype=float)
        self.spreadMap = spreadMap
        self.droneMap = np.zeros((self.n,self.m), dtype=int)
        self.viewMap = np.zeros((self.n,self.m), dtype=int)
        self.droneNumber = droneNumber
        self.dronePositions = {}
        self.noisyFireMap = np.zeros((self.n,self.m), dtype=float)
        self.fireMap = fireMap
        self.noisyMap = np.zeros((self.n, self.m), dtype=float)
    
    def initialize(self):
        if(self.droneNumber > self.n*self.m):
            print("Error: too many drones")
            return
        if(self.droneNumber > 0):
            for j in range(1, self.droneNumber+1): #for each drone place it in a random position
                startingPosition = random.randint(0, self.m)
                self.droneMap[0][startingPosition] = j
                self.dronePositions[j] = [0, startingPosition, (1,0)]
        #set noisyspreadmapm noisyfiremap equal to spreadmap, firemap but with noise
        for i in range(0,self.n):
            for j in range(0,self.m):
                self.noisyMap[i][j] = np.random.uniform(0, 1)
        #loop through noisySpreadMap and multiply noisyMap with spreadmap
        for i in range(0,self.n):
            for j in range(0,self.m):
                self.noisySpreadMap[i][j] = self.spreadMap[i][j] * self.noisyMap[i][j]

        #loop through noisyFireMap and multiply noisyMap with firemap
        for i in range(0,self.n):
            for j in range(0,self.m):
                self.noisyFireMap[i][j] = self.fireMap[i][j] * self.noisyMap[i][j]

    def updateVision(self, posy, posx, droneNo): #update the vision of the drone in the viewMap 
        #remove the old vision of the drone with the droneNo
        for i in range(0,self.n):
            for j in range(0,self.m):
                if self.viewMap[i][j] == droneNo:
                    self.viewMap[i][j] = 0
        #update the vision of the drone with the droneNo in the viewMap and update the noisySpreadMap and noisyFireMap
        for i in range(posy-self.VIEWRANGE, posy+self.VIEWRANGE+1):
            for j in range(posx-self.VIEWRANGE, posx+self.VIEWRANGE+1):
                if i >= 0 and i < self.n and j >= 0 and j < self.m:
                    self.viewMap[i][j] = droneNo
                    self.noisySpreadMap[i][j] = self.spreadMap[i][j]
                    self.noisyFireMap[i][j] = self.fireMap[i][j]
                    if(self.noisyMap[i][j] < 1):
                        if(self.noisyMap[i][j]>0.9): self.noisyMap[i][j]=1
                        else:
                            self.noisyMap[i][j]+=0.1
                    else:
                        if self.noisyMap[i][j]<1.1: self.noisyFireMap[i][j]=1
                        else:
                            self.noisyMap[i][j]-=1
        
        self.updateNoisySpreadMap()
        self.updateNoisyFireMap()
        
    def updateNoisyFireMap(self):
        #loop through noisyFireMap and multiply noisyMap with firemap
        for i in range(0,self.n):
            for j in range(0,self.m):
                self.noisyFireMap[i][j] = self.fireMap[i][j] * self.noisyMap[i][j]
    def updateNoisySpreadMap(self):
        #loop through noisySpreadMap and multiply noisyMap to it
        for i in range(0,self.n):
            for j in range(0,self.m):
                if(self.viewMap[i][j]==0): self.noisySpreadMap[i][j] = self.spreadMap[i][j] * self.noisyMap[i][j]
    
    def move(self, newSpreadMap):
        self.spreadMap=newSpreadMap
        #for each drone move it down by 1 until it has moved a distance of MOVERANGE
        if(self.droneNumber > 0):
            for j in range(1, self.droneNumber+1):
                ypos = self.dronePositions[j][0]
                xpos = self.dronePositions[j][1]
                direction = self.dronePositions[j][2]
                if direction == (1,0):
                    self.moveDown(ypos, xpos, j)

                elif direction == (-1,0):
                    self.moveUp(ypos, xpos, j)
            
        else:
            self.updateNoisySpreadMap()
            self.updateNoisyFireMap()

    def moveDown(self, ypos,  xpos, droneNo):
        remainingMoves = self.MOVERANGE
        for i in range(ypos+1, ypos+self.MOVERANGE): #move the drone down
                        if i >= 0 and i < self.n:
                            self.droneMap[i-1][xpos] = 0 #remove the drone from the old position
                            self.droneMap[i][xpos] = droneNo #place the drone in the new position
                            self.dronePositions[droneNo] = [i, xpos, (1,0)] #update the position of the drone
                            self.updateVision(i, xpos, droneNo) #update the vision of the drone
                            remainingMoves -= 1
                        else: 
                            for k in range(1,remainingMoves): 
                                self.droneMap[i-k][xpos] = 0
                                self.droneMap[i-k-1][xpos] = droneNo
                                self.dronePositions[droneNo] = [i-k-1, xpos, (1,0)]
                                self.updateVision(i-k-1, xpos, droneNo)
                            self.dronePositions[droneNo][2] = (-1,0)
                            break
    def moveUp(self, ypos, xpos,droneNo):
                remainingMoves = self.MOVERANGE
                for i in range(ypos-1, ypos-self.MOVERANGE, -1): #move the drone up (reversed loop order)
                    if i >= 0 and i < self.n:
                        self.droneMap[i+1][xpos] = 0 
                        self.droneMap[i][xpos] = droneNo
                        self.dronePositions[droneNo] = [i, xpos,(-1,0)]
                        self.updateVision(i, xpos, droneNo)
                        remainingMoves -= 1
                    else:
                        for k in range(1,remainingMoves):
                            self.droneMap[i+k][xpos] = 0
                            self.droneMap[i+k+1][xpos] = droneNo
                            self.dronePositions[droneNo] = [i+k+1, xpos, (-1,0)]
                            self.updateVision(i+k+1, xpos, droneNo)
                        self.dronePositions[droneNo][2] = (1,0)
                        break


                


        

        
