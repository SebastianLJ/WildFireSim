import numpy as np
import random

class WindModel():
    def __init__(self, n, m, seed):
        self.n = n
        self.m = m
        self.seed = seed
        np.random.seed(self.seed)
        random.seed(self.seed)
        self.windSpeed = random.random()
        self.generate_wind_vector()

    def print_settings(self):
        print("Wind vector: ", self.wind_vector)
        print("Vector angle: ", self.get_wind_vector_angle())
        print("Wind angle min: ", self.get_wind_angle_min())
        print("Wind angle max: ", self.get_wind_angle_max())
        print("Normalized Wind speed: ", self.windSpeed)
        print("Wind speed: ", self.windSpeed*30, "m/s")


    def get_wind_radius(self):
        if self.windSpeed < 0.25:
            return 2
        elif self.windSpeed < 0.5:
            return 2.5
        elif self.windSpeed < 0.75:
            return 3
        else:
            return 4
        
    def generate_wind_vector(self):
        a = np.random.uniform(-1, 1)
        b = np.random.uniform(-1, 1)
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
        if self.wind_vector[0] == 0 and self.wind_vector[1] == 0:
            return 0
        return (self.get_wind_vector_angle() - self.get_wind_speed_factor() / 2) % 360

    def get_wind_angle_max(self):
        if self.wind_vector[0] == 0 and self.wind_vector[1] == 0:
            return 0
        return (self.get_wind_vector_angle() + self.get_wind_speed_factor() / 2) % 360