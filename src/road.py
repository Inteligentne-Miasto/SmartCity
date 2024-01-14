import pygame

from config import *
from lane import Lane

class Road:
    def __init__(self, model, start_intersection, end_intersection, x, y, direction):
        self.model = model
        self.start_intersection = start_intersection
        self.end_intersection = end_intersection
        self.x = x
        self.y = y
        self.direction = direction
        self.name = f'{self.start_intersection.name}-{self.end_intersection.name}'
        self.lanes = []
        self.create_lanes()

    def add_car(self, car):
        for lane in self.lanes:
            if lane.previous.id == car.previous.id and lane.current.id == car.current.id and lane.next.id == car.next.id:
                for i in range(len(lane.cars)):
                    if lane.cars[i] == None:
                        car.lane = lane
                        car.index = i
                        lane.cars[i] = car
                        return  
                break

    def add_car_to_lane(self, car, lane_index):
        if 0 <= lane_index < len(self.lanes):
            lane = self.lanes[lane_index]
            lane.add_car(car)
        else:
            print(f"Lane index {lane_index} is out of range for road {self.name}")
            
    def draw(self, screen):
        for i in range(len(self.lanes)):
            self.lanes[i].draw(screen, self.x, self.y, i, self.direction)


    def create_lanes(self):
        xc = self.start_intersection.x
        yc = self.start_intersection.y
        xp = self.end_intersection.x
        yp = self.end_intersection.y
        if xc == xp:
            if self.start_intersection.name == 'X':
                p1 = self.side_road('N')
                p2 = [self.start_intersection for i in range(3)]
            elif self.end_intersection.name == 'X':
                p1 = [self.end_intersection for i in range(3)]
                p2 = self.side_road('S')
            else:
                p1, p2 = self.main_road('vertical')
        elif yc == yp:
            if self.start_intersection.name == 'X':
                p1 = self.side_road('W')
                p2 = [self.start_intersection for i in range(3)]
            elif self.end_intersection.name == 'X':
                p1 = [self.end_intersection for i in range(3)]
                p2 = self.side_road('E')
            else:
                p1, p2 = self.main_road('horizontal')
        
        for p in p1:
            self.lanes.append(Lane(self.model, self, self.start_intersection, self.end_intersection, p))
        for p in p2:
            self.lanes.append(Lane(self.model, self, self.end_intersection, self.start_intersection, p))

    def main_road(self, direction):
        if direction == 'vertical':
            p1 = [self.end_intersection.next_intersection('W'),
                self.end_intersection.next_intersection('S'),
                self.end_intersection.next_intersection('E')]
            p2 = [self.start_intersection.next_intersection('W'),
                self.start_intersection.next_intersection('N'),
                self.start_intersection.next_intersection('E')]
            return p1, p2
        elif direction == 'horizontal':
            p1 = [self.end_intersection.next_intersection('S'),
                self.end_intersection.next_intersection('E'),
                self.end_intersection.next_intersection('N')]
            p2 = [self.start_intersection.next_intersection('S'),
                self.start_intersection.next_intersection('W'),
                self.start_intersection.next_intersection('N')]
            
            return p1, p2

    def side_road(self, direction   ):
        if direction == 'N':
            return [self.end_intersection.next_intersection('W'),
                self.end_intersection.next_intersection('S'),
                self.end_intersection.next_intersection('E')]
        elif direction == 'S':
            return [self.start_intersection.next_intersection('W'),
                self.start_intersection.next_intersection('N'),
                self.start_intersection.next_intersection('E')]
        elif direction == 'W':
            return [self.end_intersection.next_intersection('S'),
                self.end_intersection.next_intersection('E'),
                self.end_intersection.next_intersection('N')]
        elif direction == 'E':
            return [self.start_intersection.next_intersection('S'),
                self.start_intersection.next_intersection('W'),
                self.start_intersection.next_intersection('N')]
        pass

    def __str__(self):
        return f'R:{self.start_intersection.name}-{self.end_intersection.name}:{self.x}-{self.y}'
    
    def __repr__(self):
        return f'R:{self.start_intersection.name}-{self.end_intersection.name}:{self.x}-{self.y}'