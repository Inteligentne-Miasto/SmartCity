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
        self.run()
        

    def run(self):
        pygame.init()
        
        while self.running:
            self.handle_events(pygame.event.get())
            # Do logical updates here.
            self.simulate()

            self.screen.fill("green")  # Fill the display with a solid color
            # Render the graphics here.
            self.draw()

            # pygame.display.update()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

    def simulate(self):

        self.simulate_traffic()
        
        self.simulate_cars()

        if self.cycel == CYCLE_TIME * 4:
            self.cycel == 0
        
        self.cycel += 1

    def simulate_cars(self):
        for road in self.model.roads:
            for lane in road.lanes:
                # Gather all cars in the lane
                cars_in_lane = [car for car in lane.cars if car is not None]

                # Sort cars by their index (position in the lane)
                sorted_cars = sorted(cars_in_lane, key=lambda car: car.index)
              
                # Move each car in the sorted order
                for car in sorted_cars:
                    car.move()

        # for car in self.cars:
        #     car.move()
    def simulate_traffic_smart(self):
        # for lane in self.traffic_smart:
            
        pass
    

    def simulate_traffic(self):
        self.reset_traffic()
        for traffic in self.traffics[self.cycel//CYCLE_TIME % 4]:
            # print(f"self.tracffics: {self.traffics}")
            # print(f"self.trafic_smart: {self.traffic_smart}")
            
            traffic.change_traffic()

    def reset_traffic(self):
        for t in self.traffics:
            for traffic in t:
                traffic.color = False 
                
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