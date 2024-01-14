import pygame

from config import *
from traffic import Traffic

class Lane:
    def __init__(self, model, road, previous, current, next):
        self.model = model
        self.road = road 
        self.previous = previous
        self.current = current
        self.next = next
        self.direction = self.get_direction()
        self.traffic = self.add_traffic()
        self.cars = [None for i in range(10)]

    def add_car_to_last_index(self, car, last=False):
        if last:
            if self.cars[0] is None:
                self.cars[0] = car
                car.lane = self
                car.index = 0
                return True
            else:
                return False
            
            return None
        # Check the last position in the lane's spots
        if self.cars[-1] is None:
            self.cars[-1] = car  # Place the car at the last position
            car.lane = self
            car.index = len(self.cars) - 1  # Index of the last position
            return True  # Car added successfully
        else:
            return False
    
    def add_traffic(self):
        traffic = Traffic(self, self.road)
        if self.previous.x == self.current.x == self.next.x:
            self.model.traffics[0].append(traffic)
        elif self.previous.y == self.current.y == self.next.y:
            self.model.traffics[1].append(traffic)
        elif self.previous.x == self.current.x:
            if self.previous.y > self.current.y:
                if self.next.x > self.current.x:
                    self.model.traffics[2].append(traffic)
                else:
                    self.model.traffics[3].append(traffic)
            else:
                if self.next.x < self.current.x:
                    self.model.traffics[2].append(traffic)
                else:
                    self.model.traffics[3].append(traffic)
        elif self.previous.y == self.current.y:
            if self.previous.x > self.current.x:
                if self.next.y > self.current.y:
                    self.model.traffics[2].append(traffic)
                else:
                    self.model.traffics[3].append(traffic)
            else:
                if self.next.y < self.current.y:
                    self.model.traffics[2].append(traffic)
                else:
                    self.model.traffics[3].append(traffic)
        return traffic

    def get_direction(self):
        if self.previous.x == self.current.x:
            if self.previous.y > self.current.y:
                return 'N'
            else:
                return 'S'
        elif self.previous.y == self.current.y:
            if self.previous.x > self.current.x:
                return 'W'
            else:
                return 'E'
        else:
            return None

    def draw(self, screen, x, y, i, direction):
        if direction == 'horizontal':
            height = MODULE_HEIGHT // 10
            width = MODULE_WIDTH
            x = ((x-1) * MODULE_WIDTH)
            y = ((y-1) * MODULE_HEIGHT) + (9-i-2)*height
        if direction == 'vertical':
            height = MODULE_HEIGHT
            width = MODULE_WIDTH // 10
            x = ((x-1) * MODULE_WIDTH) + (i+2)*width
            y = ((y-1) * MODULE_HEIGHT)
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 0)

        for i in range(len(self.cars)):
            if self.cars[i] != None:
                self.cars[i].draw(screen, x, y, i, self.direction)
        
        self.traffic.draw(screen, x, y, self.direction)
                
    def __str__(self):
        return f'L:{self.previous.id}-{self.current.id}-{self.next.id}'
    
    def __repr__(self):
        return f'L:{self.previous.id}-{self.current.id}-{self.next.id}'
        