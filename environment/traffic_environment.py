import pygame
import sys



# Constants for colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)



class Intersection:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.traffic_light_state = "RED"
        self.green_light_duration = 5  # Default green light duration in seconds
        self.waiting_times = []  # List to store waiting times from vehicles

    def set_traffic_light_state(self, state):
        # Set the traffic light state (GREEN, YELLOW, RED)
        self.traffic_light_state = state

    def get_traffic_light_state(self):
        # Get the current traffic light state
        return self.traffic_light_state

    def add_waiting_time(self, waiting_time):
        # Add waiting time from a vehicle to the list
        self.waiting_times.append(waiting_time)

    def get_waiting_times(self):
        # Return the list of waiting times
        return self.waiting_times

    def clear_waiting_times(self):
        # Clear the list of waiting times
        self.waiting_times.clear()

    def extend_green_light_duration(self, duration):
        # Extend the green light duration by the specified seconds
        self.green_light_duration += duration

    def reset_green_light_duration(self):
        # Reset the green light duration to the default value
        self.green_light_duration = 5


    def visualize(self):
        pygame.init()
        screen_size = (400, 400)
        screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Traffic Simulation")

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(WHITE)

            # Draw traffic light based on its state
            if self.traffic_light_state == "RED":
                color = RED
            elif self.traffic_light_state == "GREEN":
                color = GREEN
            else:
                color = YELLOW

            pygame.draw.circle(screen, color, (200, 200), 50)  # Traffic light

            pygame.display.flip()
            clock.tick(60)


class TrafficLight:
    def __init__(self):
        self.state = "RED"

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state
