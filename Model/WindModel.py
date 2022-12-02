import numpy as np
import random

class WindModel():
    NONE, N, NE, E, SE, S, SW, W, NW = range(9)
    def __init__(self, n, m, seed):
        self.n = n
        self.m = m
        self.seed = seed
        np.random.seed(self.seed)
        random.seed(self.seed)
        #self.windDirection = random.randrange(0,8)
        self.windDirection = self.N
        #self.windSpeed = random.random()
        self.windSpeed = 0.6
        #self.generate_wind_vector()
        self.wind_vector = (0,1)
        print("Wind vector: ", self.wind_vector)
        print("Vector angle: ", self.get_wind_vector_angle())
        print("Wind angle min: ", self.get_wind_angle_min())
        print("Wind angle max: ", self.get_wind_angle_max())
        print("Wind direction: ", self.windDirection)
        print("Wind speed: ", self.windSpeed*30, "m/s")
        print("Normalized Wind speed: ", self.windSpeed)

    def get_direction(self, i,j):
        if i < 0 and j == 0:
            return self.S
        elif i < 0 and j > 0:
            return self.SW
        elif i == 0 and j > 0:
            return self.W
        elif i > 0 and j > 0:
            return self.NW
        elif i > 0 and j == 0:
            return self.N
        elif i > 0 and j < 0:
            return self.NE
        elif i == 0 and j < 0:
            return self.E
        elif i < 0 and j < 0:
            return self.SE
        else:
            return self.NONE

    def get_wind_coefficient(self, x, y):
        if self.windDirection != self.NONE and self.windDirection == self.get_direction(x,y):
            return self.windSpeed
        else:
            return 1

    def get_wind_radius(self):
        if self.windSpeed < 0.25:
            return 2
        elif self.windSpeed < 0.5:
            return 2.5
        elif self.windSpeed < 0.75:
            return 3
        else:
            return 3.5
        

    def generate_wind_vector(self):
        a = np.random.rand()
        b = np.random.rand()
        self.wind_vector = (a,b)

    def get_wind_vector_angle(self):
        vector_angle = np.arctan2(self.wind_vector[1], self.wind_vector[0])
        vector_angle %= 2*np.pi
        degs = np.degrees(vector_angle)
        return degs

    def get_wind_speed_factor(self):
        if self.windSpeed == 0:
            return 360
        elif self.windSpeed < 0.25:
            return 250
        elif self.windSpeed < 0.5:
            return 140
        elif self.windSpeed < 0.75:
            return 80
        else: 
            return 50

    def get_wind_angle_min(self):
        return (self.get_wind_vector_angle() - self.get_wind_speed_factor() / 2) % 360

    def get_wind_angle_max(self):
        return (self.get_wind_vector_angle() + self.get_wind_speed_factor() / 2) % 360