import time
import random

class VehicleAgent:
    def __init__(self, id, intersection):
        self.id = id
        self.intersection = intersection

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
