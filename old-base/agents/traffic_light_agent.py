import time
import random

# Maximum waiting time threshold
max_waiting_time = 15 #seconds

class TrafficLightAgent:
    def __init__(self, intersection, id):
        self.intersection = intersection
        self.id = id
        self.waiting_times = []  # List to store waiting times from vehicles


    def receive_waiting_time(self, waiting_time):
        # Logic to handle waiting time received from the vehicle agent
        # For example, adjust traffic light timings based on waiting time
        # Store waiting time received from a vehicle
        self.waiting_times.append(waiting_time)
        print(f"Traffic Light Agent {self.id} received waiting time: {waiting_time}")
        pass

    def adjust_light_timings(self):
        # Logic to adjust traffic light timings based on waiting times and other factors
        # Implement your coordination strategy here
        # Adjust traffic light timings based on waiting times
        current_state = self.intersection.get_traffic_light_state()
        
        # Get the total waiting time from vehicles
        total_waiting_time = sum(self.intersection.get_waiting_times())
        
        # Extend green light duration if waiting time exceeds the threshold
        if total_waiting_time > max_waiting_time:
            if current_state == "GREEN":
                self.intersection.extend_green_light_duration(5)  # Extend green light by 5 seconds
        else:
            # Reset the green light duration to the default value if waiting time is within the threshold
            self.intersection.reset_green_light_duration()
        pass

    def run(self):
        while True:
            # Static traffic light timings (simplified)
            self.intersection.set_traffic_light_state("GREEN")
            print(f"Traffic Light Agent {self.id}: GREEN")
            time.sleep(5)  # Green light duration
            
            self.intersection.set_traffic_light_state("YELLOW")
            print(f"Traffic Light Agent {self.id}: YELLOW")
            time.sleep(2)  # Yellow light duration
            
            self.intersection.set_traffic_light_state("RED")
            print(f"Traffic Light Agent {self.id}: RED")
            time.sleep(3)  # Red light duration
