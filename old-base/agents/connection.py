from spade import agent
from spade.message import Message
import asyncio

class TrafficLightAgent(agent.Agent):
    agents = [
        "TLAgent-1@localhost",
        "TLAgent-2@localhost",
        "TLAgent-3@localhost",
        "TLAgent-4@localhost",
    ]
    async def setup(self):
        print("Traffic Light Agent is ready.")

class VehicleAgent(agent.Agent):
    agents = [
        "Vehicle-1@localhost",
        "Vehicle-2@localhost",
        "Vehicle-3@localhost",
        "Vehicle-4@localhost",
        "Vehicle-5@localhost",
        "Vehicle-6@localhost",
        "EmergencyVehicle@localhost"
    ]

    async def setup(self):
        print("Vehicle Agent is ready.")

async def setup_agents():
    # Traffic Light Agent setup
    # list with all the agents
    traffic_light_agents = [ TrafficLightAgent(agent_jid, "password") for agent_jid in TrafficLightAgent.agents ]
    # start all the agents
    await asyncio.gather(*[ agent.start() for agent in traffic_light_agents ])

    # Vehicle Agent setup
    # list all the agents on a list
    vehicle_agent = [ VehicleAgent(agent_jid, "password") for agent_jid in VehicleAgent.agents ]
    # start all the agents
    await asyncio.gather(*[ agent.start() for agent in vehicle_agent ])

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(setup_agents())
    asyncio.get_event_loop().run_forever()
