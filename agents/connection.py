from spade import agent
from spade.message import Message
import asyncio

class TrafficLightAgent(agent.Agent):
    async def setup(self):
        print("Traffic Light Agent is ready.")

class VehicleAgent(agent.Agent):
    async def setup(self):
        print("Vehicle Agent is ready.")

async def setup_agents():
    # Traffic Light Agent setup
    traffic_light_agent = TrafficLightAgent("traffic_light_agent@localhost", "password")
    await traffic_light_agent.start()

    # Vehicle Agent setup
    vehicle_agent = VehicleAgent("vehicle_agent@localhost", "password")
    await vehicle_agent.start()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(setup_agents())
    asyncio.get_event_loop().run_forever()
