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
        # Removed redundant check for self.next as it's already handled below
        # print(f"self.index = {self.index} self.next = {self.next} self.route = {self.route}")
        if self.index == 0:
            if not self.can_proceed_based_on_traffic_light():
                return  # Samochód czeka, jeśli światło jest czerwone

            if self.next is None:
                self.handle_final_movement()
                return None
            else:
                prev_intersection, curr_intersection, next_intersection = self.previous, self.current, self.next
        
            next_lane = self.find_next_lane(prev_intersection, curr_intersection, next_intersection)
            # print(f"next_lane = {next_lane}")
            if "X" in str(next_intersection):
                #czy kończy trasę
                if self.lane:
                    self.lane.cars[self.index] = None
            else:
                #wiemy że następny pas istnieje
                new_temp_prev , new_temp_curr, new_temp_next = self.get_temporary_new_coords(next_lane)
                new_temp_lane = self.find_next_lane(new_temp_prev, new_temp_curr, new_temp_next, temp=True)
                if new_temp_lane and new_temp_lane.cars[-1] is None:
                    self.update_position_coords(next_lane)
                    self.update_position_on_board(next_lane)

            

        else:
            # if self.lane:
            if self.lane.cars[self.index - 1] is None:
                self.lane.cars[self.index] = None
                self.index -= 1
                self.lane.cars[self.index] = self
            else:
                pass
           

    def handle_final_movement(self):
        pass
        # ostatnie trzy skrzyżowania dają przedostatni pas ruchu
        

    def can_proceed_based_on_traffic_light(self):
        if self.current == self.lane.model.middle_intersection:
            return self.lane.traffic_smart.get_traffic()
        elif self.lane and self.lane.traffic:
            # Return True if the traffic light color is green, False otherwise
            return self.lane.traffic.get_traffic()  # True for green, False for red
        else:
            # If there is no traffic light, allow the car to proceed
            return True
  
            
    def update_position_coords(self, next_lane):
    
        self.previous = self.current
        self.current = self.next
        try:
            self.next = self.route[self.route.index(self.current) + 1]
            next_index = self.route.index(self.current) + 1
            self.next = self.route[next_index] if next_index < len(self.route) else None
            return True
        except Exception as e:
            self.next = None
            return False

    def get_temporary_new_coords(self, next_lane):
        previous = self.current
        current = self.next
        try:
            nextt = self.route[self.route.index(self.current) + 1]
            next_index = self.route.index(self.current) + 2
            nextt = self.route[next_index] if next_index < len(self.route) else None
            # print(f"temporary new coords = previous = {previous} current = {current} nextt = {nextt}")
        except Exception as e:
            nextt = None
        return previous, current, nextt

    def update_position_on_board(self, next_lane):
 
        # if self.next is not None: #nie usuwaj samochodu z ostatniego pasa
        if self.lane is not None and self.index is not None:
            self.lane.cars[self.index] = None

        if self.next is not None:      
            next_lane = self.find_next_lane(self.previous, self.current, self.next)
            if next_lane is not None:
                # print(f"update_position_on_board next_lane = {next_lane} self.next = {self.next}")
                next_lane.add_car_to_last_index(self)
        else:   
            self.handle_final_movement()

    def find_next_lane(self, previous, current, next, temp=False):


        prev_intersection = str(previous).split(":",1)[1]
        curr_intersection = str(current).split(":",1)[1]
        next_intersection = str(next).split(":",1)[1]
        new_lane = "L:" + prev_intersection + "-" + curr_intersection + "-" + next_intersection
      
        if not temp:
            # print("not temp")
            current_road = self.current.get_road(self.previous)
        else:
            # print("temp")
            # print(f"self.current = {self.current} self.previous = {self.previous} self.next = {self.next}")
            current_road = self.next.get_road(self.current)


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