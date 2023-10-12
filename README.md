# Multi Agent System Work
Work for the course of Introduction to Intelligent Autonomous Systems (CC3042) of University of Porto

---

## THEME: A. Multi-Agent Traffic Control Simulation

#### Overview
The aim is to design and implement a multi-agent system to efficiently manage traffic across multiple intersections. The agents should communicate with each other and coordinate to manage traffic signals, aiming to minimize waiting times and enhance traffic flow.

#### Objectives
Implement intelligent traffic light agents that can adapt to real-time traffic conditions.
Use vehicle agents that generate simplified but realistic traffic patterns.
Integrate these agents to work in a coordinated way to optimize traffic flow.
#### Features
Traffic Environment: The environment where the agents live can be based on a grid-like set of roads and intersections.
Traffic Light Agents: Each traffic light intersection is controlled by an agent. The agent manages the light timings (Red, Green, Yellow) based on the current traffic conditions and in coordination with other intersection agents.
Vehicle Agents: Simulate vehicle agents approaching the intersections and reacting to the traffic lights. They can report waiting times and perhaps even request green lights if waiting time exceeds a certain limit.
Central Coordination Agent: This agent gathers data from Traffic Light Agents and perhaps also the Vehicle Agents to manage larger traffic patterns or to intervene in special circumstances (like emergency vehicles coming through).
Emergency Vehicle Priority: Implement a feature where emergency vehicles (ambulance, fire brigade, police) have the highest priority and can interact with the Traffic Light Agents to ensure they get a green light.
Real-Time Adjustments: Traffic light agents could adapt to traffic conditions, perhaps changing the time the light stays green or red based on the traffic volume.
Performance Metrics: Implement metrics to measure the efficiency of traffic management in terms of waiting time, the number of vehicles going through, etc.
