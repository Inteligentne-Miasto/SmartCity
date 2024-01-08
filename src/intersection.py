import pygame
from config import *

class Intersection:
    def __init__(self, model, map, name, x, y):
        self.model = model
        self.map = map
        self.name = name
        self.x = x
        self.y = y
        self.id = f'{name}:{self.x}-{self.y}'

    def draw(self, screen):
        x = (self.x-1) * MODULE_WIDTH
        y = (self.y-1) * MODULE_HEIGHT
        size = MODULE_HEIGHT
        pygame.draw.rect(screen, (100, 100, 100), (x, y, size, size), 0)


    def get_road(self, next_intersection):
        x = next_intersection.x
        y = next_intersection.y
        if self.x == x:
            if self.y > y:
                return self.map[self.y-1][self.x]
            else:
                return self.map[self.y+1][self.x]
        elif self.y == y:
            if self.x > x:
                return self.map[self.y][self.x-1]
            else:
                return self.map[self.y][self.x+1]
        else:
            return None
    
    def get_intersection(self, x, y):
        return self.map[y][x]

    def next_intersection(self, direction):
        if direction == 'N' and self.y > 0:
            return self.get_intersection(self.x, self.y-2)
        elif direction == 'S' and self.y < len(self.map) - 1:
            return self.get_intersection(self.x, self.y+2)
        elif direction == 'W' and self.x > 0:
            return self.get_intersection(self.x-2, self.y)
        elif direction == 'E' and self.x < len(self.map) - 1:
            return self.get_intersection(self.x+2, self.y)
        else:
            return None

    def __str__(self):
        return f'I:{self.id}'    
    
    def __repr__(self):
        return f'I:{self.id}'    
    