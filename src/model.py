import random

from config import *
from tabulate import tabulate
from intersection import Intersection
from road import Road
from car import Car

class Model:
    def __init__(self):
        self.size = (GRID_SIZE + 1) * 2 + 1
        self.grid = self.create_grid()
        self.map = [[None for i in range(self.size)] for j in range(self.size)]
        self.intersections = []
        self.roads = []
        self.cars = []
        self.traffics = [[],[],[],[]]
        self.traffic_smart = [[],[],[],[]]
        self.create_intersections()

        self.middle_intersection = self.map[self.size//2][self.size//2]

        self.create_roads()
        self.create_cars()
        print(tabulate(self.map))

    def create_grid(self):
        grid = []
        m = self.size // 2
        for i in range(self.size):
            t = []
            if i % 2 == 0:
                for j in range(self.size):
                    if (i == 0 or i == self.size-1 or j == 0 or j == self.size-1):
                        t.append('X') if j % 2 == 0 else t.append('')
                    else:
                        if j % 2 == 0:
                            n = int(abs(m-i)//2) if i < m else 0
                            s = int(abs(m-i)//2) if i > m else 0
                            w = int(abs(m-j)//2) if j < m else 0
                            e = int(abs(m-j)//2) if j > m else 0
                            s = 'N'*n+'S'*s+'W'*w+'E'*e if n+s+w+e > 0 else 'M'
                            t.append(s)
                        else:
                            t.append('+')
            else:
                for j in range(self.size):
                    if j % 2 == 0 and not (j == 0 or j == self.size-1):
                        t.append('+')
                    else:
                        t.append('')
            grid.append(t)
        grid[0][0] = None
        grid[0][self.size-1] = None
        grid[self.size-1][0] = None
        grid[self.size-1][self.size-1] = None
        return grid

    def create_intersections(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] != '' and self.grid[i][j] != '+':
                    intersection = Intersection(self, self.map, self.grid[i][j], j, i)
                    self.map[i][j] = intersection
                    self.intersections.append(intersection)

    def create_roads(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == '+':
                    direction = ''
                    if i % 2 == 0:
                        direction = 'horizontal'
                        start = self.map[i][j-1]
                        end = self.map[i][j+1]
                    else:
                        direction = 'vertical'
                        start = self.map[i-1][j]
                        end = self.map[i+1][j]
                    road = Road(self, start, end, j, i, direction)
                    self.map[i][j] = road
                    self.roads.append(road)

    def create_cars(self):
        for i in range(CAR_COUNTER):
            route = []
            start = self.randomize_starting_intersection()
            route.append(start)

            if start.x == 0:
                route.append(start.next_intersection('E'))
            elif start.x == self.size-1:
                route.append(start.next_intersection('W'))
            elif start.y == 0:
                route.append(start.next_intersection('S'))
            elif start.y == self.size-1:
                route.append(start.next_intersection('N'))

            end = True
            while end:
                
                next_intersection = self.randomize_intersection(route[-1])
                if next_intersection not in route:
                    if next_intersection.name == 'X':
                        route.append(next_intersection)
                        end = False
                    else: 
                        route.append(next_intersection)
            car = Car(route)
            self.cars.append(car)
        # print(self.cars)
    
    def randomize_starting_intersection(self):
        while True:
            x = random.randint(0, self.size-1)
            y = random.randint(0, self.size-1)
            if self.map[y][x] != None:  
                if self.map[y][x].name == 'X':
                    return self.map[y][x]

    def randomize_intersection(self, intersection):
        r = random.randint(0, 3)
        if r == 0:
            return intersection.next_intersection('N')
        elif r == 1:
            return intersection.next_intersection('S')
        elif r == 2:
            return intersection.next_intersection('W')
        elif r == 3:
            return intersection.next_intersection('E')

    def __str__(self):
        return tabulate(self.map)

    def __repr__(self): 
        return tabulate(self.map)    