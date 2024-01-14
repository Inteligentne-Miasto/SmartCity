import pygame

from config import *

class Car:
    def __init__(self, route):
        self.route = route
        self.previous = route[0]
        self.current = route[1]
        self.next = route[2]
        self.lane = None
        self.index = None
        self.initialize()

    def move(self):
        print("move")
        # Removed redundant check for self.next as it's already handled below

        if self.index == 0:

            if self.next is None:
                #TODO: zrobić ruch na ostatim lane, chwilowo udajemy że go nie ma :)
                self.lane.cars[self.index] = None
                return None
            else:
                prev_intersection, curr_intersection, next_intersection = self.previous, self.current, self.next

            # Find the next lane based on the selected intersections
            next_lane = self.find_next_lane(prev_intersection, curr_intersection, next_intersection)
            if next_lane:
                self.update_position_coords(next_lane)
                self.update_position_on_board(next_lane)

        else:
            # Move the car within the current lane
            self.lane.cars[self.index] = None
            self.index -= 1
            self.lane.cars[self.index] = self

            

  
            
    def update_position_coords(self, next_lane):
        self.previous = self.current
        self.current = self.next
        try:
            self.next = self.route[self.route.index(self.current) + 1]
            next_index = self.route.index(self.current) + 1
            self.next = self.route[next_index] if next_index < len(self.route) else None
        except Exception as e:
            self.next = None

    def update_position_on_board(self, next_lane, last=False):   
        if last:
            print("last")
            print("Update position on board")
            print(f"self.lane = {self.lane} self.index = {self.index}")
            if self.lane is not None and self.index is not None:
                print('LAAAAAST')
                print(f"self.lane = {self.lane}")
                print(f"self.index = {self.index}")
                print(f"self.lane.cars = {self.lane.cars}")
                self.lane.cars[self.index] = None
                next_lane.add_car_to_last_index(self, last=True)

            return None


        # print(f"self.lane = {self.lane}")
        print("Update position on board NOT LAST")
        print(f"self.lane = {self.lane} self.index = {self.index}")
        if self.lane is not None and self.index is not None:
            print(f"self.lane = {self.lane}")
            print(f"self.index = {self.index}")
            print(f"self.lane.cars = {self.lane.cars}")
            self.lane.cars[self.index] = None

        # Przypisanie samochodu do nowego pasa i aktualizacja jego pozycji
        self.lane = next_lane
        # print(f"after change to next_lane self.lane = {self.lane}")
        if next_lane is not None:
            # print(f"next_lane = {next_lane}")
            # print(f"next_lane.cars = {next_lane.cars}")
            next_lane.add_car_to_last_index(self)

    def find_next_lane(self, previous, current, next):
        
        prev_intersection = str(previous).split(":",1)[1]
        curr_intersection = str(current).split(":",1)[1]
        print(f"find lane next = {next}")
        next_intersection = str(next).split(":",1)[1]
        new_lane = "L:" + prev_intersection + "-" + curr_intersection + "-" + next_intersection
      
        current_road = self.current.get_road(self.previous)

        road_lanes = [str(lane) for lane in current_road.lanes]
        if new_lane in road_lanes:
            # print("new_lane in road_lanes")
            return current_road.lanes[road_lanes.index(new_lane)]

        else:
            # print("new_lane not in road_lanes")
            return None
    


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