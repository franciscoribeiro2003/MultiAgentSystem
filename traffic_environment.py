import random
import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import asyncio
import spade
import pygame

# Seed the random number generator with the current system time
random.seed(time.time())

traffic_lights_grid = [[None for _ in range(100)] for _ in range(100)]
vehicles_grid = [[None for _ in range(100)] for _ in range(100)]
lanes_grid = [[None for _ in range(100)] for _ in range(100)]
intersections_grid = [[None for _ in range(100)] for _ in range(100)]

class Map:
    def __init__(self):
        pass


    def update_traffic_lights(self, x, y, info):
        traffic_lights_grid[x][y] = info

    def update_vehicles(self, x, y, info):
        vehicles_grid[x][y] = info

    def update_lanes(self, x, y, info):
        if lanes_grid[x][y] is None:
            lanes_grid[x][y] = [] 
        
        lanes_grid[x][y].append(info)
        

    def update_intersections(self, x, y, info):
        intersections_grid[x][y] = info
    
    def WhatsNextLane(self, x,y):
        # display the movements avaible for the car, so if it is in the intersection display the lanes that the car can go, if it is in the lane display the next lane
        # use spade to get the position of the car and sent him the next avaible positions so he can go to

        if lanes_grid[x][y] is not None:
            # if the car is in a lane
            # get the next position from the lane id
            lanes = []
            # get all the ids of the lanes_grid and then acess that lanes by id and get the next position or positions
            for i in range(len(env.lanes)):
                for k in range(len(lanes_grid[x][y])):
                    if env.lanes[i].lane_id == lanes_grid[x][y][k]:
                        lanes.append(env.lanes[i].next_position(x,y))                        
                        break
            return lanes

    def IsThereTrafficLight(self, x, y):
        # check if there is a traffic light in the position
        if traffic_lights_grid[x][y] is not None or traffic_lights_grid[x][y] != 0:
            return traffic_lights_grid[x][y]
        return False
    
    def IsThereCar(self, x, y):
        #print (f"Verificar          {x, y}, {vehicles_grid[x][y]}")
        # check if there is a car in the position
        if vehicles_grid[x][y] is None or vehicles_grid[x][y]  == 0:
            #print ("checkk")
            return False
        return vehicles_grid[x][y]


    async def draw_map(self):
        pygame.init()
        screen_width, screen_height = 1000, 1000
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Traffic Simulation')

        lane_color = (169, 169, 169)  # Gray
        intersection_color = (105, 105, 105)  # Dark Gray
        null_color = (0, 0, 0)  # Black
        car_pink = (255, 192, 203)  # Pink
        greenback = (0, 200, 100)  # Green background

        traffic_light_colors = {
            'Green': (0, 255, 0),
            'Yellow': (255, 255, 0),
            'Red': (255, 0, 0),
            'Intermitent': (255, 165, 0)  # Orange for Intermitent
        }
        running = True

        while running:
            xs = []
            ys = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(greenback)  # Green background

            # Draw grid
            cell_size = screen_width // 100  # Assuming 100x100 grid
            for x in range(100):
                for y in range(100):
                    if lanes_grid[x][y] is not None:
                        pygame.draw.rect(screen, lane_color, (x * cell_size, y * cell_size, cell_size, cell_size))

                    if intersections_grid[x][y] is not None:
                        pygame.draw.rect(screen, intersection_color, (x * cell_size, y * cell_size, cell_size, cell_size))

                    if traffic_lights_grid[x][y] is not None:
                        tl_id = (traffic_lights_grid[x][y])
                        color = 'Red' 
                        for tl in env.traffic_lights:
                            if tl.id == tl_id:
                                color = tl.get_color()
                                break
                        pygame.draw.rect(screen, traffic_light_colors[color], (x * cell_size, y * cell_size, cell_size, cell_size))

                    
                    if (vehicles_grid[x][y] is not None and vehicles_grid[x][y] != 0) :
                        print(f"painting over------{x, y}, {vehicles_grid[x][y]}")
                        pygame.draw.rect(screen, car_pink, (x * cell_size, y * cell_size, cell_size, cell_size))
                        xs.append(x)
                        ys.append(y)
                    #await asyncio.sleep(0.01)
            for i in range(len(xs)):
                    if lanes_grid[xs[i]][ys[i]] is not None:
                        pygame.draw.rect(screen, lane_color, (x * cell_size, y * cell_size, cell_size, cell_size))

                    if intersections_grid[xs[i]][ys[i]] is not None:
                        pygame.draw.rect(screen, intersection_color, (x * cell_size, y * cell_size, cell_size, cell_size))

                    if traffic_lights_grid[xs[i]][ys[i]] is not None:
                        tl_id = (traffic_lights_grid[x][y])
                        color = 'Red' 
                        for tl in env.traffic_lights:
                            if tl.id == tl_id:
                                color = tl.get_color()
                                break
                        pygame.draw.rect(screen, traffic_light_colors[color], (x * cell_size, y * cell_size, cell_size, cell_size))
                    pygame.draw.rect(screen, greenback, (x * cell_size, y * cell_size, cell_size, cell_size))
                    if (vehicles_grid[x][y] is not None and vehicles_grid[x][y] != 0) :
                        pygame.draw.rect(screen, car_pink, (x * cell_size, y * cell_size, cell_size, cell_size))

                    
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
        self.map=Map()
        self.map.update_traffic_lights(cordX, cordY, id)

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
        self.x = x
        self.y = y
        self.map=Map()
        self.map.update_intersections(x, y, name)

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
        self.map=Map()
        self.map.update_vehicles(x, y, car_id)

    def move(self, x, y):
        print(f"Car {self.car_id} moved from ({self.x},{self.y}) to ({x},{y})")
        self.x = int(x)
        self.y = int(y)
        self.map.update_vehicles(self.x, self.y, self.car_id)
        print(f"Car is in {self.x, self.y}, and the map is {vehicles_grid[self.x][self.y]}, so the car is {self.car_id}")

    def travel(self):
        whatsnextlanes = self.map.WhatsNextLane(self.x, self.y)
        if whatsnextlanes is not None:
            nextmove = random.choice(whatsnextlanes)
            return nextmove
        return None

    def IsThereTrafficLight(self, nextmove):
        if self.map.IsThereTrafficLight(nextmove[0], nextmove[1]) is not False:
            # check if there is a traffic light in the next position
            tl_id = self.map.IsThereTrafficLight(nextmove[0], nextmove[1])
            for tl in env.traffic_lights:
                if tl.id == tl_id:
                    if tl.get_color() == 'Red':
                        # if the traffic light is red, the car will wait
                        tl.num_cars_waiting += 1
                        while tl.get_color() == 'Red':
                            return True
                        tl.num_cars_waiting -= 1
                        break
                    elif tl.get_color() == 'Yellow':
                        # if the traffic light is yellow, the car will wait
                        tl.num_cars_waiting += 1
                        while tl.get_color() == 'Yellow':
                            return True
                        tl.num_cars_waiting -= 1
                        break
                    else:
                        # if the traffic light is green, the car will move
                        return False


    def IsThereCarRight(self, nextmove):
        # check if there is a car in the next position or at the right of the next position, so see the current position and the next to see what is going to be the right
        # the right of the next position should have priority so return true if there is a car in the right of the next position
        # to find the right of the next position, we need to see the current position and the next position, build a vector to find the direction of the movement, ot then see whats on the right
        vector = (nextmove[0]-self.x, nextmove[1]-self.y)
        newxplus= nextmove[0]+1
        newyplus= nextmove[1]+1
        newxminus= nextmove[0]-1
        newyminus= nextmove[1]-1

        if vector == (0,1):
            # going up (down visually)
            if (newxminus<0): return False
            if self.map.IsThereCar(nextmove[0]-1, nextmove[1]) is not False:
                return True
        elif vector == (0,-1):
            # going down (up visually)
            if (newxplus>99): return False
            if self.map.IsThereCar(nextmove[0]+1, nextmove[1]) is not False:
                return True
        elif vector == (1,0):
            # going right
            if (newyplus>99): return False
            if self.map.IsThereCar(nextmove[0], nextmove[1]+1) is not False:
                return True
        elif vector == (-1,0):
            # going left
            if (newyminus<0): return False
            if self.map.IsThereCar(nextmove[0], nextmove[1]-1) is not False:
                return True        
        if self.map.IsThereCar(nextmove[0], nextmove[1]) is not False:
            return True
        return False

    speed = 2
    async def run(self):
        while True:
            nextmove=self.travel()
            if nextmove is not None:
                if self.IsThereTrafficLight(nextmove) is not True:
                    if self.map.IsThereCar(nextmove[0], nextmove[1]) is not True:
                        if self.IsThereCarRight(nextmove) is not True:
                            pastx=self.x
                            pasty=self.y
                            self.move(nextmove[0], nextmove[1])
                            print(f"___________presente {self.x, self.y}_____________")
                            self.map.update_vehicles(pastx, pasty, 0)
                        else:
                            print(f"Car {self.car_id} is waiting for the car(s) passing by")
                            await asyncio.sleep(1)
                            continue
                    else:
                        print(f"Car {self.car_id} is waiting for the car in front to move")
                        await asyncio.sleep(1)
                        continue
                else:
                    print(f"Car {self.car_id} is waiting for the traffic light to change")
                    await asyncio.sleep(1)
                    continue
            else:
                print("No road finded, car is waiting")
                await asyncio.sleep(1)
                continue
            await asyncio.sleep(1)



        




class RoadSign:
    def __init__(self, sign_type):
        self.sign_type = sign_type


class Lane:
    def __init__(self, lane_id):
        self.lane_id = lane_id
        self.cars = []
        self.lane = []
        self.map=Map()

    def add_car(self, car):
        self.cars.append(car)

    def add_lane(self, *args):
        for lane_coord in args:
            self.lane.append(lane_coord)
            x, y = lane_coord
            self.map.update_lanes(x, y, self.lane_id)

    def next_position(self, x, y):
        # get the next position from the lane id
        for i in range(len(self.lane)):
            if int(self.lane[i][0]) == int(x) and int(self.lane[i][1]) == int(y):
                if (i+1) == len(self.lane):
                    return None
                lanes = self.lane[i+1]
                return lanes


class Road:
    def __init__(self, name, num_lanes):
        self.name = name
        self.lanes = [Lane(i) for i in range(num_lanes)]
        self.map=Map()

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

        lane1.add_lane((0,0), (0,1), (0,2), (0,3), (0,4), (1,4), (2,4), (3,4), (4,4), (5,4), (6,4), (7,4), (8,4), (9,4), (10,4), (11,4), (12,4), (13,4), (14,4), (15,4), (16,4), (17,4), (18,4), (19,4), (20,4), (21,4), (22,4), (23,4), (24,4), (25,4), (26,4), (27,4), (28,4), (29,4), (30,4), (31,4), (32,4), (33,4), (34,4), (35,4), (36,4), (37,4), (38,4), (39,4), (40,4), (41,4), (42,4), (43,4), (44,4), (45,4), (46,4), (47,4), (48,4), (49,4), (50,4), (51,4), (52,4), (53,4), (54,4), (55,4), (56,4), (57,4), (58,4), (59,4), (60,4), (61,4), (62,4), (63,4), (64,4), (65,4), (66,4), (67,4), (68,4), (69,4), (70,4), (71,4), (72,4), (73,4), (74,4), (75,4), (76,4), (77,4), (78,4), (79,4), (80,4), (81,4), (82,4), (83,4), (84,4), (85,4), (86,4), (87,4), (88,4), (89,4), (90,4), (91,4), (92,4), (93,4), (94,4), (95,4), (96,4), (97,4), (98,4), (99,4))
        lane2.add_lane((99, 3), (98, 3), (97, 3), (96, 3), (95, 3), (94, 3), (93, 3), (92, 3), (91, 3), (90, 3), (89, 3), (88, 3), (87, 3), (86, 3), (85, 3), (84, 3), (83, 3), (82, 3), (81, 3), (80, 3), (79, 3), (78, 3), (77, 3), (76, 3), (75, 3), (74, 3), (73, 3), (72, 3), (71, 3), (70, 3), (69, 3), (68, 3), (67, 3), (66, 3), (65, 3), (64, 3), (63, 3), (62, 3), (61, 3), (60, 3), (59, 3), (58, 3), (57, 3), (56, 3), (55, 3), (54, 3), (53, 3), (52, 3), (51, 3), (50, 3), (49, 3), (48, 3), (47, 3), (46, 3), (45, 3), (44, 3), (43, 3), (42, 3), (41, 3), (40, 3), (39, 3), (38, 3), (37, 3), (36, 3), (35, 3), (34, 3), (33, 3), (32, 3), (31, 3), (30, 3), (29, 3), (28, 3), (27, 3), (26, 3), (25, 3), (24, 3), (23, 3), (22, 3), (21, 3), (20, 3), (19, 3), (18, 3), (17, 3), (16, 3), (15, 3), (14, 3), (13, 3), (12, 3), (11, 3), (10, 3), (9, 3), (8, 3), (7, 3), (6, 3), (5, 3), (4, 3), (3, 3), (2, 3), (1, 3), (1, 2), (1, 1), (1, 0))

        road_2.add_lane(lane3)
        road_2.add_lane(lane4)

        # other positions
        lane4.add_lane((0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9), (5,10), (5,11), (5,12), (5,13), (5,14), (5,15), (5,16), (5,17), (5,18), (5,19), (5,20), (5,21), (5,22), (5,23), (5,24), (5,25), (5,26), (5,27), (5,28), (5,29), (5,30), (5,31), (5,32), (5,33), (5,34), (5,35), (5,36), (5,37), (5,38), (5,39), (5,40), (5,41), (5,42), (5,43), (5,44), (5,45), (5,46), (5,47), (5,48), (5,49), (5,50), (5,51), (5,52), (5,53), (5,54), (5,55), (5,56), (5,57), (5,58), (5,59), (5,60), (5,61), (5,62), (5,63), (5,64), (5,65), (5,66), (5,67), (5,68), (5,69), (5,70), (5,71), (5,72), (5,73), (5,74), (5,75), (5,76), (5,77), (5,78), (5,79), (5,80), (5,81), (5,82), (5,83), (5,84), (5,85), (5,86), (5,87), (5,88), (5,89), (5,90), (5,91), (5,92), (5,93), (5,94), (5,95), (5,96), (5,97), (5,98), (5,99))
        lane3.add_lane((6, 99), (6, 98), (6, 97), (6, 96), (6, 95), (6, 94), (6, 93), (6, 92), (6, 91), (6, 90), (6, 89), (6, 88), (6, 87), (6, 86), (6, 85), (6, 84), (6, 83), (6, 82), (6, 81), (6, 80), (6, 79), (6, 78), (6, 77), (6, 76), (6, 75), (6, 74), (6, 73), (6, 72), (6, 71), (6, 70), (6, 69), (6, 68), (6, 67), (6, 66), (6, 65), (6, 64), (6, 63), (6, 62), (6, 61), (6, 60), (6, 59), (6, 58), (6, 57), (6, 56), (6, 55), (6, 54), (6, 53), (6, 52), (6, 51), (6, 50), (6, 49), (6, 48), (6, 47), (6, 46), (6, 45), (6, 44), (6, 43), (6, 42), (6, 41), (6, 40), (6, 39), (6, 38), (6, 37), (6, 36), (6, 35), (6, 34), (6, 33), (6, 32), (6, 31), (6, 30), (6, 29), (6, 28), (6, 27), (6, 26), (6, 25), (6, 24), (6, 23), (6, 22), (6, 21), (6, 20), (6, 19), (6, 18), (6, 17), (6, 16), (6, 15), (6, 14), (6, 13), (6, 12), (6, 11), (6, 10), (6, 9), (6, 8), (6, 7), (6, 6), (6, 5), (6, 4), (6, 3), (6, 2), (6, 1), (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0))



        
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

        self.car2 = Car(2, 2, 1)
        self.car3= Car(3, 5, 4)
        self.car1 = Car(1, 0, 0)

        self.cars = [self.car1, self.car2, self.car3]

        self.map=Map()

        
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
        simulation_task = asyncio.create_task(env.map.draw_map())
        intersection_task = asyncio.create_task(env.intersections[0].run())
        car_task2 = asyncio.create_task(env.car2.run())
        car_task3 = asyncio.create_task(env.car3.run())
        car_task1 = asyncio.create_task(env.car1.run())


        await asyncio.gather(intersection_task, simulation_task, car_task1, car_task2, car_task3)

    asyncio.run(main())