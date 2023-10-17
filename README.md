# Multi Agent System Work
Work for the course of Introduction to Intelligent Autonomous Systems (CC3042) of University of Porto

---
## Tech Stack:
- XMPP Server (Prosody) - ejabberd
- Python-Spade


---
## THEME: A. Multi-Agent Traffic Control Simulation

### Overview
The aim is to design and implement a multi-agent system to efficiently manage traffic across multiple intersections. The agents should communicate with each other and coordinate to manage traffic signals, aiming to minimize waiting times and enhance traffic flow.


### Objectives
Implement intelligent traffic light agents that can adapt to real-time traffic conditions.
Use vehicle agents that generate simplified but realistic traffic patterns.
Integrate these agents to work in a coordinated way to optimize traffic flow.


### Features
Traffic Environment: The environment where the agents live can be based on a grid-like set of roads and intersections.
Traffic Light Agents: Each traffic light intersection is controlled by an agent. The agent manages the light timings (Red, Green, Yellow) based on the current traffic conditions and in coordination with other intersection agents.
Vehicle Agents: Simulate vehicle agents approaching the intersections and reacting to the traffic lights. They can report waiting times and perhaps even request green lights if waiting time exceeds a certain limit.
Central Coordination Agent: This agent gathers data from Traffic Light Agents and perhaps also the Vehicle Agents to manage larger traffic patterns or to intervene in special circumstances (like emergency vehicles coming through).
Emergency Vehicle Priority: Implement a feature where emergency vehicles (ambulance, fire brigade, police) have the highest priority and can interact with the Traffic Light Agents to ensure they get a green light.
Real-Time Adjustments: Traffic light agents could adapt to traffic conditions, perhaps changing the time the light stays green or red based on the traffic volume.
Performance Metrics: Implement metrics to measure the efficiency of traffic management in terms of waiting time, the number of vehicles going through, etc.

---
## Milestones
### Week 1: Research & Planning

Research SPADE/JADE features and functionalities.
Define roles and functionalities for different agents.

### Week 2-3: Basic Implementations

Implement the traffic environment.    
Implement basic Traffic Light Agents.
Implement simple Vehicle Agents.

### Week 4: Intermediate Implementations

Implement communication between agents.
Design and implement coordination strategies for Traffic Light Agents.

### Week 5: Advanced Features

Introduce the Central Coordination Agent.
Implement emergency vehicle priority.
Implement rerouting for Vehicle Agents in reaction to traffic conditions.

### Week 6: Testing & Documentation

Final testing and debugging.
Document the code and prepare a presentation reporting the work done.


---
## Step-by-step

### 1. Understand the Requirements:
Familiarize yourself thoroughly with the project requirements, objectives, and features. Understand the role of each agent and how they interact with one another.

### 2. Set Up the Tech Stack:
XMPP Server (Prosody/ejabberd): Set up a server for communication between agents.
Python-Spade: Install and configure the Python-Spade framework, which will be used to create intelligent agents.

### 3. Design the System Architecture:
Plan the overall architecture of your multi-agent system. Define the roles and responsibilities of each agent.
Identify the message-passing protocols between agents. Decide how agents will communicate with each other.

### 4. Implement Traffic Environment:
Design a grid-based road and intersection system. This could be a simple matrix representation.
Implement the environment where agents (traffic lights and vehicles) will operate.

### 5. Implement Traffic Light Agents:
Create intelligent traffic light agents. Implement logic for managing light timings based on traffic conditions.
Allow the agents to communicate with each other to coordinate timings and optimize traffic flow.

### 6. Implement Vehicle Agents:
Simulate vehicle agents that approach intersections. Implement logic for vehicle behavior based on traffic lights.
Vehicles should report waiting times and request green lights if waiting time exceeds a certain limit.

### 7. Implement Central Coordination Agent:
Create a central coordination agent responsible for gathering data from Traffic Light Agents and Vehicle Agents.
Implement logic for managing larger traffic patterns and intervening in special circumstances.

### 8. Implement Emergency Vehicle Priority:
Implement a feature where emergency vehicles have the highest priority.
Allow emergency vehicles to interact with Traffic Light Agents to ensure they get a green light.

### 9. Implement Real-Time Adjustments:
Implement logic for traffic light agents to adapt to real-time traffic conditions.
Agents should be able to change light timings based on traffic volume and other dynamic factors.

### 10. Implement Performance Metrics:
Implement metrics to measure the efficiency of traffic management.
Metrics could include waiting time, the number of vehicles passing through intersections, etc.

### 11. Testing and Debugging:
Test the system extensively under various scenarios and conditions.
Debug and optimize the system for performance and efficiency.
