import pygame
from .map import Map
from .car import Car
import time

class SimulationHandler():
    def __init__(self):
        self.width_px = 1280
        self.height_px = 720
        self.car = Car((600,600))
        self.map = Map(self.width_px, self.height_px, self.car, (255, 255, 255), (128, 128, 128))

        pygame.init()
        self.screen = pygame.display.set_mode((self.width_px, self.height_px))
        self.screen.fill((255, 255, 255))
        self.clock = pygame.time.Clock()
    
    def initialize(self):
        self.map.draw_race_track(self.screen)

    # this method is called from the get_raw_fitness method in the network class from neat, it returns the fitness of the network
    def start_episode(self, network):

        # set car to initial position
        self.car.reset_position()
        
        # an episode is a test drive of the car; an episode ends when the car finished or got to the goal
        # with each frame the network gets inputs like sensor values and generates outputs like speed, steering brakes

        running = True

        fitness = 0

        while running:
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # get map environment data
            environment = self.map.load_environment(self.screen)

            # load current sensor data from car
            sensor_data = self.car.get_sensor_data(environment, self.screen)

            # feed sensor data to network and generate output
            output = network.compute_inputs(sensor_data[0], sensor_data[1], sensor_data[2], sensor_data[3])
            speed = output[0]
            steering = output[1]

            # feed sensor data to network and get output

            
            # handle network fitness tracking


            # rerender map
            self.map.render(self.screen)
        
            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        return fitness
        #pygame.quit()