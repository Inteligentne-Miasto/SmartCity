import pygame

from config import *
from model import Model

class Simulation:
    def __init__(self):
        self.model = Model()
        self.map = self.model.map
        self.cars = self.model.cars
        self.traffics = self.model.traffics
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
        # sort list of cars
        pass

    def simulate_traffic(self):
        self.reset_traffic()
        for traffic in self.traffics[self.cycel//CYCLE_TIME % 4]:
            traffic.change_traffic()

    def reset_traffic(self):
        for t in self.traffics:
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