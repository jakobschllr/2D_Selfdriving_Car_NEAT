import pygame
from .map import Map
from .car import Car
import time

class SimulationHandler():
    def __init__(self):
        self.width_px = 1280
        self.height_px = 720
        self.car_start_position = (600,600)
        self.car = Car(self.car_start_position)
        self.map = Map(self.width_px, self.height_px, self.car, (255, 255, 255), (128, 128, 128))
        pygame.init()
        self.screen = pygame.display.set_mode((self.width_px, self.height_px))
        self.screen.fill((255, 255, 255))
        self.clock = pygame.time.Clock()

        self.current_generation = 0
        self.current_network = 0

    def initialize(self):
        self.map.draw_race_track(self.screen)

    # this method is called from the get_raw_fitness method in the network class from neat, it returns the fitness of the network
    def start_episode(self, network, generation):
        
        # update generation and network counters
        if self.current_generation != generation:
            self.current_network = 0
        else:
            self.current_network += 1
        self.current_generation = generation

        # set car to initial position
        #self.car.reset_position(self.car_start_position)
        self.car = Car(self.car_start_position)
        self.map.car = self.car
        
        # an episode is a test drive of the car; an episode ends when the car finished or got to the goal
        # with each frame the network gets inputs like sensor values and generates outputs like speed, steering brakes

        running = True

        distance_traveled = 0
        start_time = time.time()

        stagnation_counter = 0
        last_position = None
        current_position = None

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
            output = network.compute_inputs(sensor_data[0] / self.car.sensor_reach, sensor_data[1] / self.car.sensor_reach, sensor_data[2] / self.car.sensor_reach, sensor_data[3] / self.car.sensor_reach)
            speed = output[0]
            steering = output[1]

            #print("Network Output Speed: ", speed)
            #print("Network Output Steering: ", steering)
            #print("Car position: ", (self.car.x_position, self.car.y_position))

            # move car based on networks decision
            self.car.steer(2*steering-1) # scale value to be between -1 and 1
            self.car.move_forward(speed)

            last_position = (current_position)
            current_position = (round(self.car.x_position), round(self.car.y_position))

            if current_position == last_position:
                stagnation_counter += 1
            else:
                stagnation_counter = 0
            
            # handle network fitness tracking
            if self.car.hit_obstacle:
                running = False
            elif stagnation_counter == 5:
                running = False
                distance_traveled = 0
            else:
                distance_traveled += speed

            # rerender map
            self.map.render(self.screen, self.current_generation, self.current_network)
        
            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60
            #time.sleep(0.2)

        endtime = time.time()
        survival_time = endtime - start_time

        del self.car

        print("Fitness: ", survival_time * distance_traveled) 

        return survival_time * distance_traveled
        #pygame.quit()