import pygame

from config import *
from model import Model

class Simulation:
    def __init__(self):
        self.model = Model()
        self.map = self.model.map
        self.cars = self.model.cars
        self.traffics = self.model.traffics
        self.traffic_smart = self.model.traffic_smart
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.cycel = 0
        #############Below are variables for smart traffic
        self.selected_lane = None
        self.previous_selected_nr_cyklu = None
        self.selected_lane_cycles = 5
        ##############################
        self.run()
        
        
        

    def run(self):
        pygame.init()

        while self.running:
            self.handle_events(pygame.event.get())
            self.simulate()
            self.screen.fill("green")  
            # Render the graphics here.
            self.draw()

            # pygame.display.update()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def simulate(self):

        self.simulate_traffic()
        self.simulate_traffic_smart()
        self.simulate_cars()

        if self.cycel == CYCLE_TIME * 4:
            self.cycel == 0
        
        self.cycel += 1

    def simulate_cars(self):
        for road in self.model.roads:
            for lane in road.lanes:
                
                cars_in_lane = [car for car in lane.cars if car is not None]

                sorted_cars = sorted(cars_in_lane, key=lambda car: car.index)
              
                for car in sorted_cars:
                    car.move()


    def simulate_traffic_smart(self):
        # Skip lane selection if the current lane is still within its 3-cycle active period
        if self.selected_lane_cycles < 3:
            self.selected_lane_cycles += 1
        else:
            # Reset for the next selection
            self.selected_lane = None
            self.selected_lane_cycles = 0

            lanes_with_car_counts = []
            for road in self.model.roads:
                        if "M" in str(road):
                            for lane in road.lanes:
                                cars_in_lane = [car for car in lane.cars if car is not None]
                                lanes_with_car_counts.append((lane, len(cars_in_lane)))

            # Sort and find the busiest lane
            lanes_with_car_counts.sort(key=lambda x: x[1], reverse=True)

            # Find the busiest lane that doesn't have the same nr_cyklu as the previously selected lane
            for lane, _ in lanes_with_car_counts:
                if lane.nr_cyklu != self.previous_selected_nr_cyklu and lane.cars and lane.cars[0] is not None:
                    self.selected_lane = lane
                    break

            # If no new lane meets the condition, try to find a different lane
            if not self.selected_lane:
                for lane, _ in lanes_with_car_counts:
                    if lane.nr_cyklu != self.previous_selected_nr_cyklu:
                        self.selected_lane = lane
                        break

            if self.selected_lane:
                self.previous_selected_nr_cyklu = self.selected_lane.nr_cyklu


        # Change traffic lights based on the selected lane
        self.reset_traffic_smart()
        if self.selected_lane:
            for traffic in self.traffic_smart[self.selected_lane.nr_cyklu]:
                traffic.change_traffic()
            # print(f"Selected lane for smart traffic: {self.selected_lane}")
            # print(f"nr cyklu: {self.selected_lane.nr_cyklu}")
        else:
            print("No suitable lane found for smart traffic.")
                   

    def simulate_traffic(self):
        self.reset_traffic()
        for traffic in self.traffics[self.cycel//CYCLE_TIME % 4]:            
            traffic.change_traffic()

    def reset_traffic(self):
        for t in self.traffics:
            for traffic in t:
                traffic.color = False 

    def reset_traffic_smart(self):          
        for t in self.traffic_smart:
            for traffic in t:
                traffic.color = False 

    def draw(self):
        for i in self.model.intersections:
            i.draw(self.screen)
        for r in self.model.roads:
            r.draw(self.screen)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

Simulation()