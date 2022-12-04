import numpy as np
import random
 
class DroneModel():
    VIEWRANGE = 1 #need to ome up with better estimate. 
    MOVERANGE = 3 #7.2 km/h
 
    def __init__(self, n, m, seed, spreadMap, fireMap, droneNumber):
        self.n = n
        self.m = m
        self.seed = seed
        np.random.seed(self.seed)
        random.seed(self.seed)
        self.noisySpreadMap = np.zeros((self.n,self.m), dtype=float)
        self.spreadMap = spreadMap
        self.droneMap = [[set() for i in range(self.n)] for j in range(self.m)]
        self.viewMap = np.zeros((self.n,self.m), dtype=int)
        self.droneNumber = droneNumber
        self.dronePositions = {}
        self.noisyFireMap = np.zeros((self.n,self.m), dtype=float)
        self.fireMap = fireMap
        self.noisyMap = np.zeros((self.n, self.m), dtype=float)
 
    def initialize(self):
        #loop through the dronemap and initialize each entry with empty set
        for i in range(0, self.n):
            for j in range(0, self.m):
                self.droneMap[i][j] = set()
        if(self.droneNumber > self.n*self.m):
            print("Error: too many drones")
            return
        if(self.droneNumber > 0):
            for j in range(1, self.droneNumber+1): #for each drone place it in a random position
                startingPosition = random.randint(0, self.m-1)
                self.droneMap[0][startingPosition].add(j)
                self.dronePositions[j] = [0, startingPosition, (1,1)]
        #set noisyspreadmapm noisyfiremap equal to spreadmap, firemap but with noise
        for i in range(0,self.n):
            for j in range(0,self.m):
                self.noisyMap[i][j] = np.random.uniform(0, 1.5)
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
                        if self.noisyMap[i][j]<1.1: self.noisyMap[i][j]=1
                        else:
                            self.noisyMap[i][j]-=0.1
 
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
                if direction[0] == 1:
                    self.moveDown(ypos, xpos, j, self.MOVERANGE)
 
                elif direction[0] == -1:
                    self.moveUp(ypos, xpos, j, self.MOVERANGE)
                  
        self.updateNoisySpreadMap()
        self.updateNoisyFireMap()


    def moveDown(self, ypos,  xpos, droneNo, remainingMoves):
        remainingMoves = self.MOVERANGE
        for i in range(ypos+1, ypos+remainingMoves): #move the drone down
                        if i >= 0 and i < self.n:
                            self.droneMap[i-1][xpos].remove(droneNo) #remove the drone from the old position
                            self.droneMap[i][xpos].add(droneNo) #place the drone in the new position
                            self.dronePositions[droneNo][0]=i
                            self.dronePositions[droneNo][1] = xpos
                            self.updateVision(i, xpos, droneNo) #update the vision of the drone
                        else: 
                            if i-1+self.VIEWRANGE>=self.n-1 and xpos+self.VIEWRANGE>=self.m-1: #if the drone is at the bottom right corner
                                self.dronePositions[droneNo][2] = (-1,-1)
                                self.moveUp(i-1, xpos, droneNo,(ypos+remainingMoves)-i)
                                break
                            elif i-1>=self.n-1 and xpos-self.VIEWRANGE <= 0:
                                if self.dronePositions[droneNo][2][1] == -1: ##going tothe left
                                    self.droneMap[i-1][xpos].remove(droneNo) #remove the drone from the map
                                    self.droneMap[i-1][xpos+2*self.VIEWRANGE].add(droneNo) #place the drone in the new position
                                    self.dronePositions[droneNo] = [i-1, xpos+2*self.VIEWRANGE, (1,1)]
                                    self.updateVision(i-1, xpos+2*self.VIEWRANGE, droneNo)
                                    self.moveUp(i-1, xpos + 2 * self.VIEWRANGE, droneNo, (ypos+remainingMoves)-i)
                                    break
                                else:
                                    self.droneMap[i-1][xpos].remove(droneNo)
                                    self.droneMap[i-1][xpos+2*self.VIEWRANGE].add(droneNo)
                                    self.dronePositions[droneNo]=[i-1,xpos+2*self.VIEWRANGE, (-1,1)]
                                    self.updateVision(i-1, xpos+2*self.VIEWRANGE, droneNo)
                                    self.moveUp(i - 1,xpos+2*self.VIEWRANGE, droneNo, (ypos+remainingMoves)-i)
                                    break
                            elif self.dronePositions[droneNo][2] == (1, -1): #direction is (1, -1) go left
                                self.droneMap[i-1][xpos].remove(droneNo) #remove the drone from the map
                                self.droneMap[i-1][xpos-2*self.VIEWRANGE].add(droneNo) #place the drone in the new position
                                self.dronePositions[droneNo] = [i-1, xpos-2*self.VIEWRANGE, (-1,-1)]
                                self.updateVision(i-1, xpos-2*self.VIEWRANGE, droneNo)
                                self.moveUp(i-1, xpos-2*self.VIEWRANGE, droneNo,ypos+remainingMoves-i)
                                break
                            else: #direction is (1,1) go right
                                if self.dronePositions[droneNo][2]==(-1, -1):
                                    self.droneMap[i-1][xpos].remove(droneNo)
                                    self.droneMap[i-1][xpos - 2*self.VIEWRANGE].add(droneNo)
                                    self.dronePositions[droneNo]=[i-1, xpos -2*self.VIEWRANGE, (-1, -1)]
                                    self.updateVision(i-1, xpos-2*self.VIEWRANGE, droneNo)
                                    self.moveUp(i-1, xpos-2*self.VIEWRANGE, droneNo)
                                    break
                                else:
                                    if xpos + 2 * self.VIEWRANGE > self.m -1:
                                        self.droneMap[i-1][xpos].remove(droneNo) # remove the drone from the map
                                        self.droneMap[i-1][self.m-1-self.VIEWRANGE].add(droneNo) # place the drone in the new position
                                        self.dronePositions[droneNo] = [i-1, self.m-1-self.VIEWRANGE, (-1, 1)]
                                        self.updateVision(i-1, self.m-1-self.VIEWRANGE, droneNo)
                                        self.moveUp(i-1, self.m-1-self.VIEWRANGE, droneNo, ypos+remainingMoves-i)
                                        break
                                    else:
                                        self.droneMap[i-1][xpos].remove(droneNo) # remove the drone from the map
                                        self.droneMap[i-1][xpos + 2*self.VIEWRANGE].add(droneNo) # place the drone in the new position
                                        self.dronePositions[droneNo] = [i-1, xpos + 2*self.VIEWRANGE, (-1, 1)]
                                        self.updateVision(i-1, xpos + 2*self.VIEWRANGE, droneNo)
                                        self.moveUp(i-1, xpos+2*self.VIEWRANGE, droneNo, ypos+remainingMoves-i)
                                        break

    def moveUp(self, ypos, xpos,droneNo, remainingMoves):
                for i in range (ypos-1, ypos-remainingMoves, -1):
                    if i >= 0 and i < self.n:
                        self.droneMap[i+1][xpos].remove(droneNo) #remove the drone from the old position
                        self.droneMap[i][xpos].add(droneNo) #place the drone in the new position
                        self.dronePositions[droneNo][0] = i
                        self.dronePositions[droneNo][1] = xpos
                        self.updateVision(i, xpos, droneNo)
                    else:
                        if i+1-self.VIEWRANGE<=0 and xpos-self.VIEWRANGE<=0: #if the drone is at the top left corner
                            self.dronePositions[droneNo][2] = (1,1)
                            self.moveDown(i + 1, xpos, droneNo, abs((ypos-remainingMoves)-i))
                            break
                        elif i+1-self.VIEWRANGE<=0 and xpos+self.VIEWRANGE >= self.m-1:
                            if self.dronePositions[droneNo][2][1] == -1: ##going tothe left
                                self.droneMap[i+1][xpos].remove(droneNo) #remove the drone from the map
                                self.droneMap[i+1][xpos-2*self.VIEWRANGE].add(droneNo) #place the drone in the new position
                                self.dronePositions[droneNo] = [i+1, xpos-2*self.VIEWRANGE, (1,-1)]
                                self.updateVision(i+1, xpos-2*self.VIEWRANGE, droneNo)
                                self.moveDown(i+1, xpos - 2 * self.VIEWRANGE, droneNo, abs((ypos-remainingMoves)-i))
                                break
                            else:
                                self.droneMap[i+1][xpos].remove(droneNo)
                                self.droneMap[i+1][self.m-1-self.VIEWRANGE].add(droneNo)
                                self.dronePositions[droneNo]=[i+1, self.m-1-self.VIEWRANGE, (1,1)]
                                self.updateVision(i+1, self.m-1-self.VIEWRANGE, droneNo)
                                self.moveDown(i + 1,self.m-1-self.VIEWRANGE, droneNo, abs((ypos-remainingMoves)-i))
                                break
                        elif self.dronePositions[droneNo][2] == (-1, -1): #direction is (-1, -1) go left
                            self.droneMap[i+1][xpos].remove(droneNo) #remove the drone from the map
                            self.droneMap[i+1][xpos-2*self.VIEWRANGE].add(droneNo) #place the drone in the new position
                            self.dronePositions[droneNo] = [i+1, xpos-2*self.VIEWRANGE, (1,-1)]
                            self.updateVision(i+1, xpos-2*self.VIEWRANGE, droneNo)
                            self.moveDown(i+1, xpos - 2*self.VIEWRANGE, droneNo, abs((ypos-remainingMoves)-i))
                            break
                        else:
                            self.droneMap[i+1][xpos].remove(droneNo)
                            if xpos+2*self.VIEWRANGE > self.m-1:
                                self.droneMap[i+1][self.m-1-self.VIEWRANGE].add(droneNo)
                                self.dronePositions[droneNo]=[i+1, self.m-1-self.VIEWRANGE, (1, 1)]
                                self.updateVision(i+1, self.m-1-self.VIEWRANGE, droneNo)
                                self.moveDown(i+1, self.m-1-self.VIEWRANGE, droneNo, abs((ypos-remainingMoves)-i))
                                break
                            else:
                                self.droneMap[i+1][xpos+2*self.VIEWRANGE].add(droneNo)
                                self.dronePositions[droneNo]=[i+1, xpos+2*self.VIEWRANGE, (1, 1)]
                                self.updateVision(i+1, xpos+2*self.VIEWRANGE, droneNo)
                                self.moveDown(i+1, xpos+2*self.VIEWRANGE, droneNo, abs((ypos-remainingMoves)-i))
                                break
                        



 
 
 
 
 
 
