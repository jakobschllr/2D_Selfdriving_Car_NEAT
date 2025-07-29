import math
import numpy as np
from .sensor import Sensor
import pygame

PI = math.pi

class Car():
    def __init__(self, starting_point):
        self.angle = PI + (PI/2) # im Bogenmaß
        self.x_position = starting_point[0]
        self.y_position = starting_point[1]
        self.color = "Blue"
        self.front_color = "Red"
        self.width = 15
        self.height = 30
        self.sensor_reach = 40
        self.sensors = {
            "s1": Sensor("front-left", self.sensor_reach),
            "s2": Sensor("front-right", self.sensor_reach),
            "s3": Sensor("side-left", self.sensor_reach),
            "s4": Sensor("side-right", self.sensor_reach)
        }

    def get_car_corners(self):
        corner_1 = np.array([ -self.width, -self.height])
        corner_2 = np.array([self.width, -self.height])
        corner_3 = np.array([self.width, self.height])
        corner_4 = np.array([-self.width, self.height])

        rotation_matrix = np.array([[math.cos(self.angle), -math.sin(self.angle)],
                  [math.sin(self.angle), math.cos(self.angle)]
                  ])

        rotated_corner_1 = np.dot(rotation_matrix, corner_1)
        rotated_corner_2 = np.dot(rotation_matrix, corner_2)
        rotated_corner_3 = np.dot(rotation_matrix, corner_3)
        rotated_corner_4 = np.dot(rotation_matrix, corner_4)

        return [rotated_corner_1, rotated_corner_2, rotated_corner_3, rotated_corner_4]


    def reset_position(self):
        self.position = (80,80)


    def move_forward(self, speed):
        # speed goes from 1 pixel per frame to 10 pixels per frame
        angle = self.angle - PI/2

        self.x_position -= math.cos(angle) * speed
        self.y_position -= math.sin(angle) * speed

    def steer(self, value):
        # value goes from -1.0 (left) to 1.0 (right)
        self.angle += value * math.pi / 5

    def get_sensor_data(self, environment, screen):
        sensor_data = []
        for sensor in self.sensors.values():
            distance = sensor.get_distance(self.angle, (self.x_position, self.y_position), environment, screen)
            sensor_data.append(distance)
        
        return sensor_data