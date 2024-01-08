import pygame

from config import *

class Car:
    def __init__(self, route):
        self.route = route
        self.previous = route[0]
        self.current = route[1]
        self.next = route[2]
        self.lane = None
        self.initialize()

    def initialize(self):
        road = self.previous.get_road(self.current)
        road.add_car(self)

    def draw(self, screen, x, y, i, direction):
        height = MODULE_HEIGHT // 10
        width = MODULE_WIDTH // 10
        if direction == 'N':
            x = x
            y = y + (i)*height
            a = (x, y+height)
            b = (x+width//2, y)
            c = (x+width, y+height)
        elif direction == 'S':
            x = x
            y = y + (9-i)*height
            a = (x+width, y)
            b = (x+width//2, y+height)
            c = (x, y)
        elif direction == 'W':
            x = x + (i)*width
            y = y
            a = (x+width, y+height)
            b = (x, y+height//2)
            c = (x+width, y)
        elif direction == 'E':
            x = x + (9-i)*height
            y = y
            a = (x, y)
            b = (x, y+height)
            c = (x+width, y+height//2)
            pass
        # pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 1)
        pygame.draw.polygon(screen, (0,0,255), [a, b, c])

    def __str__(self):
        return f'{self.route}'
    
    def __repr__(self):
        return f'{self.route}'