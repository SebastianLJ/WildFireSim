import numpy as np
import random

class DroneModel():
    def __init__(self, n, m, seed, spreadMap, noisySpreadMap, droneNumber):
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
        self.viewRange = 5
        self.moveRange = 2
        self.dronePositions = {}
    
    def initialize(self, n,m):
        for j in range(1, self.droneNumber+1): #for each drone place it in a random position
            self.droneMap[0][np.randint(0,m)] = j
            self.dronePositions[j] = [0, np.randint(0,m)]
    
    def updateVision(self, n,m, posy, posx, droneNo): #update the vision of the drone in the viewMap 
        #remove the old vision of the drone with the droneNo
        for i in range(0,n):
            for j in range(0,m):
                if self.viewMap[i][j] == droneNo:
                    self.viewMap[i][j] = 0
        #update the vision of the drone with the droneNo in the viewMap and update the noisySpreadMap
        for i in range(posy-self.viewRange, posy+self.viewRange):
            for j in range(posx-self.viewRange, posx+self.viewRange):
                if i >= 0 and i < n and j >= 0 and j < m:
                    self.viewMap[i][j] = droneNo
                    self.noisySpreadMap[i][j] = self.spreadMap[i][j]
        

            
        
    
    def move(self, n,m, posy, posx):
        #for each drone move it down by 1 until it has moved a distance of moveRange
        for j in range(self.droneNumber):
            ypos = self.dronePositions[j][0]
            xpos = self.dronePositions[j][1]
            for i in range(ypos+1, ypos+self.moveRange):
                if i >= 0 and i < n:
                    self.droneMap[i-1][xpos] = 0 #remove the drone from the old position
                    self.droneMap[i][xpos] = j #place the drone in the new position
                    self.dronePositions[j] = [i, xpos] #update the position of the drone
                    self.updateVision(n,m, i, posx) #update the vision of the drone


                


        

        
