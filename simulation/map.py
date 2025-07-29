import pygame
from .car import Car
import numpy as np

class Map():
    def __init__(self, x_limit, y_limit, car, background_color, track_color):
        self.x_limit = x_limit
        self.y_limit = y_limit
        self.car: Car = car
        self.environment = None
        self.background_color = background_color
        self.track_color = track_color
        self.surface = None

    def load_environment(self, screen):
        if self.environment == None:
            screen.lock()
            colored_pixels = set()

            for x in range(screen.get_width()):
                for y in range(screen.get_height()):
                    color = screen.get_at((x,y))
                    if color != self.background_color:
                        colored_pixels.add((round(x),round(y)))
            screen.unlock()
            self.environment = colored_pixels

        return self.environment


    # allows user to draw the race track the car should learn to drive
    def draw_race_track(self, screen):
        self.surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.surface.fill((0,0,0,0))

        # objjects for start button
        btn_rect = pygame.Rect(1100, 30, 150, 30)
        font = pygame.font.SysFont(None, 24)
        btn_text = font.render("Starte Evolution", True, (255,255,255))

        running = True
        drawing = False
        while running:
            screen.fill((255, 255, 255))
            screen.blit(self.surface, (0,0))

            # draw start button
            pygame.draw.rect(screen, "Blue", btn_rect)
            text_rect = btn_text.get_rect(center=btn_rect.center)
            screen.blit(btn_text, text_rect)

            # draw car at inital position
            self.draw_car(screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

            mouse_pos = pygame.mouse.get_pos()

            if btn_rect.collidepoint(mouse_pos):
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0]:
                    return
            
            if drawing:
                pygame.draw.circle(self.surface, self.track_color, mouse_pos, 40)

            pygame.display.flip()
    
    # renders the map, updates the position of the car and shows information
    def render(self, screen: pygame.display):

        # overwrite anything
        screen.fill((255, 255, 255))

        if self.surface:
            screen.blit(self.surface, (0,0))

        # redraw the screen with the new car position
        self.draw_car(screen)


    def draw_car(self, screen: pygame.display):

        # draw car based car position and angle
        car_corners = self.car.get_car_corners()

        for i in range(0, 4):
            if i != 2:
                start_line = (self.car.x_position + car_corners[i % 4][0], self.car.y_position + car_corners[i % 4][1])
                end_line = (self.car.x_position + car_corners[(i+1) % 4][0], self.car.y_position + car_corners[(i+1) % 4][1])
            pygame.draw.line(screen, self.car.color, start_line, end_line, width=2)

        front_line_start = (self.car.x_position + car_corners[2][0], self.car.y_position + car_corners[2][1])
        front_line_end = (self.car.x_position + car_corners[3][0], self.car.y_position + car_corners[3][1])
        pygame.draw.line(screen, self.car.front_color, front_line_start, front_line_end, width=2)
