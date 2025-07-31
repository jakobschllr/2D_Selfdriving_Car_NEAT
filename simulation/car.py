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
        self.sensor_reach = 45
        self.sensors = {
            "s1": Sensor("front-left", self.sensor_reach),
            "s2": Sensor("front-right", self.sensor_reach),
            "s3": Sensor("side-left", self.sensor_reach),
            "s4": Sensor("side-right", self.sensor_reach)
        }
        self.hit_obstacle = False

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


    def move_forward(self, speed):
        angle = self.angle - PI/2

        self.x_position -= math.cos(angle) * (speed*20)
        self.y_position -= math.sin(angle) * (speed*20)

    def steer(self, value):
        # value goes from -1.0 (left) to 1.0 (right)
        self.angle += value * math.pi / 30

    def get_sensor_data(self, environment, screen):
        sensor_data = []
        for sensor in self.sensors.values():
            distance, hit_obstacle = sensor.get_distance(self.angle, (self.x_position, self.y_position), environment, screen)
            sensor_data.append(distance)
            if hit_obstacle:
                self.hit_obstacle = True
        return sensor_data
    
    def made_significant_move(self, pos_before, pos_after):

        if pos_before != None:

            if pos_before == pos_after:
                return False  

            start_x = pos_before[0] - 20
            start_y = pos_before[1] - 20

            end_x = pos_before[0] + 20
            end_y = pos_before[1] + 20

            x = start_x
            y = start_y

            while x <= end_x:
                while y <= end_y:
                    if pos_after == (x,y):
                        print("Made no significant move")
                        return False
                    
                    y += 1
                x += 1

            return True