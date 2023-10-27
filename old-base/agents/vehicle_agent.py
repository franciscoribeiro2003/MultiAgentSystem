from calendar import c
import time
import random

class VehicleAgent:
    def __init__(self, id, intersection, x , y, roadmap):
        self.id = id
        self.intersection = intersection
        self.x = x
        self.y = y
        self.roadmap = roadmap


    def travel(self):
        # choose a coordinate from the roadmap next to the current coordinate that is given with x,y
        # check if the coordinate is a traffic light
        # if it is a traffic light, check if it is green, if it is not green, wait
        # if it is green, travel to the next coordinate
        # in a intersaction, choose randomly a direction to go to
        # if the coordinate is not a traffic light, travel to the next coordinate in the same way you are going, so dont be on a loop
        current_road = self.roadmap.get_road()
        current_x = self.x
        current_y = self.y
        current_coordinate = (current_x, current_y)
        next_coordinate = current_coordinate
        for coordinate in current_road:
            if coordinate == current_coordinate:
                next_coordinate = current_road[current_road.index(coordinate) + 1]
                break
        print(f"vehicle {self.id} is going to {next_coordinate}")
        # check if the next coordinate is a traffic light
        if next_coordinate in self.intersection.traffic_lights:
            # check if the traffic light is green
            while self.intersection.get_traffic_light_state() != "GREEN":
                print(f"vehicle {self.id} is waiting for the traffic light to turn green")
                time.sleep(1)
            # if the traffic light is green, travel to the next coordinate
            print(f"vehicle {self.id} is traveling to {next_coordinate}")
            self.x = next_coordinate[0]
            self.y = next_coordinate[1]
            # check if the next coordinate is a traffic light
            if next_coordinate in self.intersection.traffic_lights:
                # check if the traffic light is green
                while self.intersection.get_traffic_light_state() != "GREEN":
                    print(f"vehicle {self.id} is waiting for the traffic light to turn green")
                    time.sleep(1)
                # if the traffic light is green, travel to the next coordinate
                print(f"vehicle {self.id} is traveling to {next_coordinate}")
                self.x = next_coordinate[0]
                self.y = next_coordinate[1]
            else:
                print(f"vehicle {self.id} is traveling to {next_coordinate}")
                self.x = next_coordinate[0]
                self.y = next_coordinate[1]
        else:
            print(f"vehicle {self.id} is traveling to {next_coordinate}")
            self.x = next_coordinate[0]
            self.y = next_coordinate[1]

    def run(self):
        while True:
            # Vehicle approaching intersection
            time.sleep(random.randint(1, 5))  # Simulate random arrival time
            
            # Check traffic light state
            traffic_light_state = self.intersection.get_traffic_light_state()
            
            if traffic_light_state == "GREEN":
                print(f"Vehicle {self.id} passed the intersection.")
            elif traffic_light_state == "RED":
                print(f"Vehicle {self.id} is waiting at the intersection.")
                # Simulate waiting time
                time.sleep(random.randint(1, 5))
                # Request green light after waiting for some time
                if random.choice([True, False]):
                    print(f"Vehicle {self.id} requests green light.")
                    # Logic for requesting green light can be added here
                    # For simplicity, let's assume the light turns green immediately
                    self.intersection.set_traffic_light_state("GREEN")
            elif traffic_light_state == "YELLOW":
                print(f"Vehicle {self.id} should stop for the yellow light.")
