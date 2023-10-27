import threading
import time
import random
from agents.traffic_light_agent import TrafficLightAgent
from agents.vehicle_agent import VehicleAgent
from environment.traffic_environment import Intersection



# Function to simulate communication between agents
def agent_communication(traffic_light, vehicle):
    while True:
        # Vehicle informs Traffic Light Agent about waiting time
        waiting_time = random.randint(1, 10)
        traffic_light.receive_waiting_time(waiting_time)
        
        # Traffic Light Agent optimizes light timings based on waiting time
        traffic_light.adjust_light_timings()
        
        time.sleep(random.randint(3, 7))  # Wait for a random duration before the next communication


intersection1 = Intersection(1, 4, 1, 4)

intersection2 = Intersection(2, 4, 1, 3)

# Assign 4 traffic lights to the intersection1
intersection1.add_traffic_light(1, 1)
intersection1.add_traffic_light(1, 3)
intersection1.add_traffic_light(0, 2)
intersection1.add_traffic_light(2, 2)

# Assign 3 traffic lights to the intersection2
intersection2.add_traffic_light(5, 2)
intersection2.add_traffic_light(6,3)
intersection2.add_traffic_light(6, 1)

# Start creating a class for a road map, the road object should just be a list of coordinates where is possible to travel
class RoadMap:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.road = []
    
    def add_road(self, x, y):
        self.road.append((x, y))

    def get_road(self):
        return self.road

    def clear_road(self):
        self.road.clear()



# make a road map that connects the two intersections via (2,2) to (5,2)
roadmap1 = RoadMap(1, 2)
roadmap1.add_road(2, 2)
roadmap1.add_road(3, 2)
roadmap1.add_road(4, 2)
roadmap1.add_road(5, 2)
roadmap1.add_road(6, 2)
roadmap1.add_road(1,1)
roadmap1.add_road(1,3)
roadmap1.add_road(0,2)


# Create Traffic Lights Agents and Vehicle Agents instances for all the agents in connection.py
traffic_light_agent1 = TrafficLightAgent(1, intersection1)
traffic_light_agent2 = TrafficLightAgent(2, intersection1)
traffic_light_agent3 = TrafficLightAgent(3, intersection1)
traffic_light_agent4 = TrafficLightAgent(4, intersection1)

vehicle_agent1 = VehicleAgent(1, intersection1, 1, 1, roadmap1)
vehicle_agent2 = VehicleAgent(2, intersection1, 1, 3, roadmap1)
vehicle_agent3 = VehicleAgent(3, intersection1, 0, 2, roadmap1)
vehicle_agent4 = VehicleAgent(4, intersection1, 2, 2, roadmap1)
vehicle_agent5 = VehicleAgent(5, intersection2, 5, 2, roadmap1)
vehicle_agent6 = VehicleAgent(6, intersection2, 6, 3, roadmap1)

# Start threads for Traffic Light Agent, Vehicle Agent, and communication simulation
traffic_light_thread1 = threading.Thread(target=traffic_light_agent1.run)
traffic_light_thread2 = threading.Thread(target=traffic_light_agent2.run)
traffic_light_thread3 = threading.Thread(target=traffic_light_agent3.run)
traffic_light_thread4 = threading.Thread(target=traffic_light_agent4.run)

vehicle_thread1 = threading.Thread(target=vehicle_agent1.travel)
vehicle_thread2 = threading.Thread(target=vehicle_agent2.travel)
vehicle_thread3 = threading.Thread(target=vehicle_agent3.travel)
vehicle_thread4 = threading.Thread(target=vehicle_agent4.travel)
vehicle_thread5 = threading.Thread(target=vehicle_agent5.travel)
vehicle_thread6 = threading.Thread(target=vehicle_agent6.travel)

# communication thread for all the agents
communication_thread1 = threading.Thread(target=agent_communication, args=(traffic_light_agent1, vehicle_agent1))
communication_thread2 = threading.Thread(target=agent_communication, args=(traffic_light_agent2, vehicle_agent2))
communication_thread3 = threading.Thread(target=agent_communication, args=(traffic_light_agent3, vehicle_agent3))
communication_thread4 = threading.Thread(target=agent_communication, args=(traffic_light_agent4, vehicle_agent4))
communication_thread5 = threading.Thread(target=agent_communication, args=(traffic_light_agent1, vehicle_agent5))
communication_thread6 = threading.Thread(target=agent_communication, args=(traffic_light_agent2, vehicle_agent6))



# Start Pygame visualization in a separate thread
#pygame_thread1 = threading.Thread(target=intersection1.visualize)
#pygame_thread2 = threading.Thread(target=intersection2.visualize)


# Start all threads
traffic_light_thread1.start()
traffic_light_thread2.start()
traffic_light_thread3.start()
traffic_light_thread4.start()

vehicle_thread1.start()
vehicle_thread2.start()
vehicle_thread3.start()
vehicle_thread4.start()
vehicle_thread5.start()
vehicle_thread6.start()

communication_thread1.start()
communication_thread2.start()
communication_thread3.start()
communication_thread4.start()
communication_thread5.start()
communication_thread6.start()

#pygame_thread1.start()
#pygame_thread2.start()