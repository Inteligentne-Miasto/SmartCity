import pygame

from config import *

class Traffic:
    def __init__(self, lane, road):
        self.name = 'T'+str(lane)
        self.road = road
        # dodać self.intersection
        self.color = False
    
    def get_traffic(self):
        return self.color
    
    def change_traffic(self):
        self.color = not self.color

    def draw(self, screen, x, y, direction):
        r = MODULE_HEIGHT // 20
        if direction == 'N':
            x = x + r
            y = y - r
        if direction == 'S':
            x = x + r
            y = y + MODULE_HEIGHT + r
        if direction == 'W':
            x = x - r
            y = y + r
        if direction == 'E':
            x = x + MODULE_WIDTH + r
            y = y + r
        if self.color:
            pygame.draw.circle(screen, (0, 255, 0), (x, y), r)
        else:
            pygame.draw.circle(screen, (255, 0, 0), (x, y), r)

    def __str__(self):
        return f'{self.name}'