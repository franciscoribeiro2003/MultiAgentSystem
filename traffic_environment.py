import random
import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import asyncio
import spade
import pygame


# Grid of cordinates for the environment 100x100
grid = [[0 for x in range(100)] for y in range(100)]

class Map:
    def __init__(self):
        pass
        
    def whereiam(self, x, y):
        return grid[x][y]
    
    def WhatsNorth(self, x, y):
        return grid[x][y+1]

    def WhatsSouth(self, x, y):
        return grid[x][y-1]
    
    def WhatsEast(self, x, y):
        return grid[x+1][y]
    
    def WhatsWest(self, x, y):
        return grid[x-1][y]
    
    def WhatsNext(self, x,y):
        # display the movements avaible for the car, so if it is in the intersection display the lanes that the car can go, if it is in the lane display the next lane
        # use spade to get the position of the car and sent him the next avaible positions so he can go to
        vehicle_position = (x,y)
        
        if grid[x][y].split(' ')[0] == 'intersection':
            pass
            Intersection_id = grid[x][y].split(' ')[1]
            # rods from the intersection id
            roads = []
            for i in range(len(env.intersections)):
                if env.intersections[i].name == Intersection_id:
                    intersection = env.intersections[i]
                    for k in range(len(env.roads)):
                        if env.roads[k] == intersection.road1:
                            roads.append(intersection.road1)
                        elif env.roads[k] == intersection.road2:
                            roads.append(intersection.road2)
                    break
            # get the lanes from the roads
            lanes = []
            for i in range(len(roads)):
                lanes.append(roads[i].lanes)
            # return the roads.lanes avaible at the intersection
            return lanes
         
        if grid[x][y].split(' ')[0] == 'lane':
            # how to get lane id the lane i the grid is displayed like this "lane {id}", so remove the 'lane' and get the id
            lane_id = int(grid[x][y].split(' ')[1])
            # get the next position from the lane id
            
            for i in range(len(env.lanes)):
                if env.lanes[i].lane_id == lane_id:
                    lanes = [env.lanes[i].next_position(x,y)]
                    return lanes
                
        if grid[x][y].split(' ')[0] == 'traffic_light':
            # how to get lane id the lane i the grid is displayed like this "lane {id}", so remove the 'lane' and get the id
            traffic_light_id = int(grid[x][y].split(' ')[1])
            # get the next position from the lane id
            
            for i in range(len(env.traffic_lights)):
                if env.traffic_lights[i].id == traffic_light_id:
                    lanes = [env.traffic_lights[i].cordX, env.traffic_lights[i].cordY]
                    return lanes
        return 0
                    
        


    async def draw_map(self):
        pygame.init()
        screen_width, screen_height = 1000, 1000
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Traffic Simulation')

        lane_color = (169, 169, 169)  # Gray
        intersection_color = (105, 105, 105)  # Dark Gray
        null_color = (0, 0, 0)  # Black
        car_pink = (255, 192, 203)  # Pink

        traffic_light_colors = {
            'Green': (0, 255, 0),
            'Yellow': (255, 255, 0),
            'Red': (255, 0, 0),
            'Intermitent': (255, 165, 0)  # Orange for Intermitent
        }
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 255, 0))  # Green background

            # Draw grid
            cell_size = screen_width // 100  # Assuming 100x100 grid
            for x in range(100):
                for y in range(100):
                    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                    if grid[x][y] == 0:
                        pygame.draw.rect(screen, null_color, rect)
                    elif grid[x][y].split(' ')[0] == 'lane':
                        pygame.draw.rect(screen, lane_color, rect)
                    elif grid[x][y].split(' ')[0] == 'intersection':
                        pygame.draw.rect(screen, intersection_color, rect)
                    elif grid[x][y].split(' ')[0] == 'traffic_light':
                        tl_id = int(grid[x][y].split(' ')[1])
                        color = 'Red' 
                        for tl in env.traffic_lights:
                            if tl.id == tl_id:
                                color = tl.get_color()
                                break
                        pygame.draw.rect(screen, traffic_light_colors[color], rect)
                    elif grid[x][y].split(' ')[0] == 'car':
                        pygame.draw.rect(screen, car_pink, rect)
            pygame.display.flip()
            await asyncio.sleep(0.1)

        pygame.quit()


    
    
class TrafficLight:
    def __init__(self, id , intersection, colorfront, colorleft, road, cordX, cordY):
        self.id = id
        self.colorfront = colorfront
        self.colorleft = colorleft
        self.intersection = intersection
        self.num_cars_waiting = 0 # number of cars waiting at the traffic light
        self.waiting_times = []  # List to store waiting times from vehicles
        self.road = road
        self.cordX = cordX
        self.cordY = cordY
        grid[cordX][cordY] = f'traffic_light {str(self.id)}'

    def change(self, new_colorfront, new_colorleft):
        self.colorfront = new_colorfront
        self.colorleft = new_colorleft


    # Store waiting time received from a vehicle
    def receive_waiting_time(self, waiting_time):
        self.waiting_times.append(waiting_time)
        pass

    
    def asking_to_change(self):
        # Logic to handle asking to change from the vehicle agent
        # For example, adjust traffic light timings based on asking to change

        while self.colorfront == "Red":
            total_waiting_time = sum(self.intersection.get_waiting_times())
            if total_waiting_time > 60 or self.num_cars_waiting > 10:
                return True
        return False
        
    def get_waiting_times(self):
        return self.waiting_times
    
    def get_color(self):
        if self.colorfront == "Green":
            return "Green"
        elif self.colorfront == "Yellow":
            return "Yellow"
        else:
            return 'Red'
    
    def run(self):
        while True:
            self.asking_to_change()
            


class Intersection:
    def __init__(self, name, road1, road2, x, y):
        self.name = name
        self.road1 = road1
        self.road2 = road2
        self.tlights = []
        grid
        self.x = x
        self.y = y
        grid[x][y] = f'intersection {self.name}'

    # traffic lights
    def add_tlight(self, tlight):
        self.tlights.append(tlight)
    
    # Logic of the lights btween the two roads and traffic lights
    # if the road is the same btween the traffic lights, then the traffics lights will be at the same color

    def change(self, color1, color2):
        if color1 == 'Green':
            color1left = 'Intermitent'
        elif color1 == 'Yellow':
            color1left = 'Yellow'
        else :
            color1left = 'Red'

        if color2 == 'Green':
            color2left = 'Intermitent'
        elif color2 == 'Yellow':
            color2left = 'Yellow'
        else :
            color2left = 'Red'
            
        for i in range(len(self.tlights)):
            if self.tlights[i].road==self.road1:
                self.tlights[i].change(color1, color1left)
                print(f"Traffic Light Agent {self.tlights[i].id}: Front: {color1}; Left: {color1left}")

            elif self.tlights[i].road==self.road2:
                self.tlights[i].change(color2, color2left)
                print(f"Traffic Light Agent {self.tlights[i].id}: Front: {color2}; Left: {color2left}")

    async def run(self):
        while  True:
            self.change('Green', 'Red')
            print ("-------------------------------------------------------")
            await asyncio.sleep(10)
            self.change('Yellow', 'Red')
            print ("-------------------------------------------------------")
            await asyncio.sleep(3)
            self.change('Red', 'Green')
            print ("-------------------------------------------------------")
            await asyncio.sleep(10)
            self.change('Red', 'Yellow')
            print ("-------------------------------------------------------")
            await asyncio.sleep(3)
            





class Car:
    def __init__(self, car_id, x, y):
        self.car_id = car_id
        self.x = x
        self.y = y

    def move(self, x, y):
        print(f"Car {self.car_id} moved from ({self.x},{self.y}) to ({x},{y})")
        self.x = int(x)
        self.y = int(y)

    def travel(self):
        map_instance = Map()
        print (grid[self.x][self.y])
        what_next = map_instance.WhatsNext(self.x, self.y)
        
        # if its a tupple
        if len(what_next)==1: 
            self.move(what_next[0][0],what_next[0][1])
        elif len(what_next)>1:
            #choose random position from the list
            lane=random.choice(what_next)
            # find the next postion of the lane            
            # get the next position from the lane id
            lanes = [(0,0)]
            for i in range(len(env.lanes)):
                if env.lanes[i].lane_id == lane:
                    lanes = [env.lanes[i].next_position(self.x,self.y)]
                    break

            self.move(lanes[0][0],lanes[0][1])


    speed = 2
    async def run(self):
        while True:
            self.travel()
            tem=grid[self.x][self.y]
            grid[self.x][self.y]=f'car {self.car_id}'
            await asyncio.sleep(1)
            grid[self.x][self.y]=tem



        




class RoadSign:
    def __init__(self, sign_type):
        self.sign_type = sign_type


class Lane:
    def __init__(self, lane_id):
        self.lane_id = lane_id
        self.cars = []
        self.lane = []

    def add_car(self, car):
        self.cars.append(car)

    # ((x,y) , (x,y) , (x,y) , (x,y)) a car only can travel on this positions per order
    def add_lane(self, lane):
        self.lane.append(lane)
        for i in range(len(lane)):
            grid[lane[i][0]][lane[i][1]] = f"lane {str(self.lane_id)}"

    def next_position(self, x, y):
        # get the next position from the lane id
        for i in range(len(self.lane[0])):
            if int(self.lane[0][i][0]) == int(x) and int(self.lane[0][i][1]) == int(y):
                lanes = self.lane[0][i-1]
                return lanes


class Road:
    def __init__(self, name, num_lanes):
        self.name = name
        self.lanes = [Lane(i) for i in range(num_lanes)]

    def add_lane(self, lane):
        self.lanes.append(lane)
    
    




class Environment:
    def __init__(self):
        road_1 = Road("Road_1", 2)  # 2 lanes
        road_2 = Road("Road_2", 2)  # 2 lanes
        road_3 = Road("Road_3", 2)
        road_4 = Road("Road_4", 2)

        
        lane1 = Lane(1)
        lane2 = Lane(2)
        lane3 = Lane(3)
        lane4 = Lane(4)

        # making a road with lanes
        road_1.add_lane(lane1)
        road_1.add_lane(lane2)

        lane1.add_lane(((0,0), (0,1), (0,2), (0,3), (0,4), (1,4), (2,4), (3,4), (4,4), (5,4), (6,4), (7,4), (8,4), (9,4), (10,4), (11,4), (12,4), (13,4), (14,4), (15,4), (16,4), (17,4), (18,4), (19,4), (20,4), (21,4), (22,4), (23,4), (24,4), (25,4), (26,4), (27,4), (28,4), (29,4), (30,4), (31,4), (32,4), (33,4), (34,4), (35,4), (36,4), (37,4), (38,4), (39,4), (40,4), (41,4), (42,4), (43,4), (44,4), (45,4), (46,4), (47,4), (48,4), (49,4), (50,4), (51,4), (52,4), (53,4), (54,4), (55,4), (56,4), (57,4), (58,4), (59,4), (60,4), (61,4), (62,4), (63,4), (64,4), (65,4), (66,4), (67,4), (68,4), (69,4), (70,4), (71,4), (72,4), (73,4), (74,4), (75,4), (76,4), (77,4), (78,4), (79,4), (80,4), (81,4), (82,4), (83,4), (84,4), (85,4), (86,4), (87,4), (88,4), (89,4), (90,4), (91,4), (92,4), (93,4), (94,4), (95,4), (96,4), (97,4), (98,4), (99,4)))
        lane2.add_lane(((1,0), (1,1), (1,2), (1,3), (2,3), (3,3), (4,3), (5,3), (6,3), (7,3), (8,3), (9,3), (10,3), (11,3), (12,3), (13,3), (14,3), (15,3), (16,3), (17,3), (18,3), (19,3), (20,3), (21,3), (22,3), (23,3), (24,3), (25,3), (26,3), (27,3), (28,3), (29,3), (30,3), (31,3), (32,3), (33,3), (34,3), (35,3), (36,3), (37,3), (38,3), (39,3), (40,3), (41,3), (42,3), (43,3), (44,3), (45,3), (46,3), (47,3), (48,3), (49,3), (50,3), (51,3), (52,3), (53,3), (54,3), (55,3), (56,3), (57,3), (58,3), (59,3), (60,3), (61,3), (62,3), (63,3), (64,3), (65,3), (66,3), (67,3), (68,3), (69,3), (70,3), (71,3), (72,3), (73,3), (74,3), (75,3), (76,3), (77,3), (78,3), (79,3), (80,3), (81,3), (82,3), (83,3), (84,3), (85,3), (86,3), (87,3), (88,3), (89,3), (90,3), (91,3), (92,3), (93,3), (94,3), (95,3), (96,3), (97,3), (98,3), (99,3)))

        road_2.add_lane(lane3)
        road_2.add_lane(lane4)

        # other positions
        lane3.add_lane(((0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7), (6,8), (6,9), (6,10), (6,11), (6,12), (6,13), (6,14), (6,15), (6,16), (6,17), (6,18), (6,19), (6,20), (6,21), (6,22), (6,23), (6,24), (6,25), (6,26), (6,27), (6,28), (6,29), (6,30), (6,31), (6,32), (6,33), (6,34), (6,35), (6,36), (6,37), (6,38), (6,39), (6,40), (6,41), (6,42), (6,43), (6,44), (6,45), (6,46), (6,47), (6,48), (6,49), (6,50), (6,51), (6,52), (6,53), (6,54), (6,55), (6,56), (6,57), (6,58), (6,59), (6,60), (6,61), (6,62), (6,63), (6,64), (6,65), (6,66), (6,67), (6,68), (6,69), (6,70), (6,71), (6,72), (6,73), (6,74), (6,75), (6,76), (6,77), (6,78), (6,79), (6,80), (6,81), (6,82), (6,83), (6,84), (6,85), (6,86), (6,87), (6,88), (6,89), (6,90), (6,91), (6,92), (6,93), (6,94), (6,95), (6,96), (6,97), (6,98), (6,99)))
        lane4.add_lane(((0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9), (5,10), (5,11), (5,12), (5,13), (5,14), (5,15), (5,16), (5,17), (5,18), (5,19), (5,20), (5,21), (5,22), (5,23), (5,24), (5,25), (5,26), (5,27), (5,28), (5,29), (5,30), (5,31), (5,32), (5,33), (5,34), (5,35), (5,36), (5,37), (5,38), (5,39), (5,40), (5,41), (5,42), (5,43), (5,44), (5,45), (5,46), (5,47), (5,48), (5,49), (5,50), (5,51), (5,52), (5,53), (5,54), (5,55), (5,56), (5,57), (5,58), (5,59), (5,60), (5,61), (5,62), (5,63), (5,64), (5,65), (5,66), (5,67), (5,68), (5,69), (5,70), (5,71), (5,72), (5,73), (5,74), (5,75), (5,76), (5,77), (5,78), (5,79), (5,80), (5,81), (5,82), (5,83), (5,84), (5,85), (5,86), (5,87), (5,88), (5,89), (5,90), (5,91), (5,92), (5,93), (5,94), (5,95), (5,96), (5,97), (5,98), (5,99)))


        
        intersection_1 = Intersection("Intersection_1", road_1, road_2, 0,0)
        #intersection_2 = Intersection("Intersection_2", road_3, road_4)

        # data structures to keep the data related to the environment
        self.roads = [road_1, road_2, road_3, road_4]

        self.intersections = [intersection_1]

        self.lanes = [lane1, lane2, lane3, lane4]

        trafficLight1 = TrafficLight(1, intersection_1, 'Red', 'Intermitent', road_1, 4, 4)
        trafficLight2 = TrafficLight(2, intersection_1, 'Red', 'Intermitent', road_1, 7, 3)
        trafficLight3 = TrafficLight(3, intersection_1, 'Red', 'Intermitent', road_2, 6, 5)
        trafficLight4 = TrafficLight(4, intersection_1, 'Red', 'Intermitent', road_2, 5, 2)

        intersection_1.add_tlight(trafficLight1)
        intersection_1.add_tlight(trafficLight2)
        intersection_1.add_tlight(trafficLight3)
        intersection_1.add_tlight(trafficLight4)


        self.traffic_lights = [trafficLight1, trafficLight2, trafficLight3, trafficLight4]

        self.car2 = Car(2, 6, 11)
        #car1 = Car(1, 0, 0)


        
    def add_road(self, road):
        self.roads.append(road)

    def add_intersection(self, intersection):
        self.intersections.append(intersection)

    # displays the environment.
    def display(self):
        for road in self.roads:
            print(f"{road.name}: ", end='')
            for lane in road.lanes:
                print(f" Lane {lane.lane_id}", end='')
            print()

        print("Intersections: ")
        for intersection in self.intersections:
            print(f"{intersection.name} - Traffic Light: ", end='')
            for tlight in intersection.tlights:
                print(f"{tlight.id} ", end='')
            print()


if __name__ == "__main__":
    env = Environment()
    env.display()

    async def main():
        map_instance = Map()
        simulation_task = asyncio.create_task(map_instance.draw_map())
        intersection_task = asyncio.create_task(env.intersections[0].run())
        car_task = asyncio.create_task(env.car2.run())

        await asyncio.gather(intersection_task, simulation_task, car_task)

    asyncio.run(main())