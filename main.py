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

# Create an intersection
intersection = Intersection(1, 1)

# Create Traffic Light Agent and Vehicle Agent instances
traffic_light_agent = TrafficLightAgent(intersection, id=1)
vehicle_agent = VehicleAgent(id=1, intersection=intersection)

# Start threads for Traffic Light Agent, Vehicle Agent, and communication simulation
traffic_light_thread = threading.Thread(target=traffic_light_agent.run)
vehicle_thread = threading.Thread(target=vehicle_agent.run)
communication_thread = threading.Thread(target=agent_communication, args=(traffic_light_agent, vehicle_agent))


# Start Pygame visualization in a separate thread
pygame_thread = threading.Thread(target=intersection.visualize)

traffic_light_thread.start()
vehicle_thread.start()
communication_thread.start()
pygame_thread.start()