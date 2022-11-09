import numpy as np
import random

class DroneModel():
    VIEWRANGE = 5
    MOVERANGE = 2
    def __init__(self, n, m, seed, spreadMap, noisySpreadMap, fireMap, noisyFireMap, droneNumber):
        self.n = n
        self.m = m
        self.seed = seed
        np.random.seed(self.seed)
        random.seed(self.seed)
        self.spreadMap = spreadMap
        self.noisySpreadMap = noisySpreadMap
        self.droneMap = np.zeros((self.n,self.m), dtype=int)
        self.viewMap = np.zeros((self.n,self.m), dtype=int)
        self.droneNumber = droneNumber
        self.dronePositions = {}
        self.fireMap = fireMap
        self.noisyFireMap = noisyFireMap
    
    def initialize(self, n,m):
        for j in range(1, self.droneNumber+1): #for each drone place it in a random position
            self.droneMap[0][np.randint(0,m)] = j
            self.dronePositions[j] = [0, np.randint(0,m), (1,0)]
    
    def updateVision(self, posy, posx, droneNo): #update the vision of the drone in the viewMap 
        #remove the old vision of the drone with the droneNo
        for i in range(0,self.n):
            for j in range(0,self.m):
                if self.viewMap[i][j] == droneNo:
                    self.viewMap[i][j] = 0
        #update the vision of the drone with the droneNo in the viewMap and update the noisySpreadMap
        for i in range(posy-self.VIEWRANGE, posy+self.VIEWRANGE):
            for j in range(posx-self.VIEWRANGE, posx+self.VIEWRANGE):
                if i >= 0 and i < self.n and j >= 0 and j < self.m:
                    self.viewMap[i][j] = droneNo
                    self.noisySpreadMap[i][j] = self.spreadMap[i][j]
                    self.noisyFireMap[i][j] = self.fireMap[i][j]
    def move(self):
        #for each drone move it down by 1 until it has moved a distance of MOVERANGE
        for j in range(1, self.droneNumber+1):
            ypos = self.dronePositions[j][0]
            xpos = self.dronePositions[j][1]
            direction = self.dronePositions[j][2]
            if direction == (1,0):
                self.moveDown(ypos, xpos, j)

            elif direction == (-1,0):
                self.moveUp(ypos, xpos, j)

    def moveDown(self, ypos,  xpos, droneNo):
        remainingMoves = self.MOVERANGE
        for i in range(ypos+1, ypos+self.MOVERANGE): #move the drone down
                        if i >= 0 and i < self.n:
                            self.droneMap[i-1][xpos] = 0 #remove the drone from the old position
                            self.droneMap[i][xpos] = droneNo #place the drone in the new position
                            self.dronePositions[droneNo] = [i, xpos] #update the position of the drone
                            self.updateVision(i, xpos) #update the vision of the drone
                            remainingMoves -= 1
                        else: 
                            for k in range(remainingMoves): 
                                self.droneMap[i-k][xpos] = 0
                                self.droneMap[i-k-1][xpos] = droneNo
                                self.dronePositions[droneNo] = [i-k-1, xpos, (1,0)]
                                self.updateVision(i-k-1, xpos)
                            self.dronePositions[droneNo][2] = (-1,0)
                            break
    def moveUp(self, ypos, xpos,droneNo):
                remainingMoves = self.MOVERANGE
                for i in range(ypos-1, ypos-self.MOVERANGE): #move the drone up
                    if i >= 0 and i < self.n:
                        self.droneMap[i+1][xpos] = 0 
                        self.droneMap[i][xpos] = droneNo
                        self.dronePositions[droneNo] = [i, xpos]
                        self.updateVision(i, xpos)
                        remainingMoves -= 1
                    else:
                        for k in range(remainingMoves):
                            self.droneMap[i+k][xpos] = 0
                            self.droneMap[i+k+1][xpos] = droneNo
                            self.dronePositions[droneNo] = [i+k+1, xpos, (-1,0)]
                            self.updateVision(i+k+1, xpos)
                        self.dronePositions[droneNo][2] = (1,0)
                        break


                


        

        
