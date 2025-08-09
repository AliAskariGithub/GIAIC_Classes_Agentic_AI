import os
import asyncio
from dotenv import load_dotenv
from typing import List, Dict
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, handoff
from agents.run import RunConfig
from colorama import init, Fore, Style

init(autoreset=True)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in your .env file.")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

# === Tools ===
def get_flights(destination: str) -> str:
    return f"✈️ Flights to {destination}:\n- AirX: $300\n- FlyJet: $280\n- SkyHigh: $320"

def suggest_hotels(destination: str) -> str:
    return f"🏨 Hotels in {destination}:\n- GrandView Hotel: 4⭐ ($120/night)\n- CozyStay Inn: 3⭐ ($80/night)"

# === Specialized Agents ===
DestinationAgent = Agent(
    name="DestinationAgent",
    instructions="Suggest travel destinations based on user's mood or interests. Ask follow-up questions if unclear.",
    model=model
)

BookingAgent = Agent(
    name="BookingAgent",
    instructions="Simulate booking flights and hotels using tools. Use get_flights() and suggest_hotels() when user wants to book.",
    model=model,
    tools={
        "get_flights": get_flights,
        "suggest_hotels": suggest_hotels
    }
)

ExploreAgent = Agent(
    name="ExploreAgent",
    instructions="Suggest local attractions, foods, and experiences in the selected destination.",
    model=model
)

# === Travel Agent Instructions ===
TravelAgent_Instruction = """
## Advanced Travel Designer

You are an intelligent and friendly **AI Travel Designer** that helps users craft personalized travel experiences. Your role is to **understand the user's intent** and seamlessly **connect them to the right specialized agent** for the next steps in their journey planning.

### Capabilities

You have access to the following **three specialized agents**:

1. * DestinationAgent**  
   _Purpose_: Suggests travel destinations based on user interests, seasons, budgets, or special occasions.

2. * BookingAgent**  
   _Purpose_: Assists in booking **flights**, **hotels**, and **accommodation packages** based on user preferences and destination.

3. * ExploreAgent**  
   _Purpose_: Recommends **attractions**, **local food**, **cultural experiences**, and **activities** based on the chosen destination.

---

### Handoff Logic

Use the appropriate handoff function when the user's request aligns with the following criteria:

| **User Intent**                                               | **Agent**         | **Handoff Function**         |
|---------------------------------------------------------------|-------------------|-------------------------------|
| Asking about destinations, where to go, or what suits them    | `DestinationAgent`| `handoff_to_destination`     |
| Asking about booking flights, hotels, or accommodations       | `BookingAgent`    | `handoff_to_booking`         |
| Asking about activities, food, local places, or experiences   | `ExploreAgent`    | `handoff_to_explore`         |

---

### Behavior Guidelines

- Always maintain a **friendly, helpful, and curious tone**.
- If you're unsure, ask clarifying questions before proceeding.
- **Guide users to the right specialist agent** using the proper handoff function.
- When handing off, briefly explain what the next agent will do to assist.

---

### Example Interactions

**User**: "I'm thinking of taking a trip in December. Where should I go?"  
**Action**: `handoff_to_destination`

**User**: "Can you help me book a hotel in Tokyo?"  
**Action**: `handoff_to_booking`

**User**: "What are some must-see places in Istanbul?"  
**Action**: `handoff_to_explore`

---

> Your goal is to ensure a smooth, intelligent, and engaging travel planning experience by guiding users through each step with the right expert help.
"""

# === Main Travel Agent ===
TravelAgent = Agent(
    name="TravelAgent",
    instructions=TravelAgent_Instruction,
    model=model,
    handoffs=[
        handoff(DestinationAgent, tool_name_override="handoff_to_destination", tool_description_override="Handoff to DestinationAgent for destination suggestions"),
        handoff(BookingAgent, tool_name_override="handoff_to_booking", tool_description_override="Handoff to BookingAgent for flight and hotel bookings"),
        handoff(ExploreAgent, tool_name_override="handoff_to_explore", tool_description_override="Handoff to ExploreAgent for attractions and experiences"),
    ]
)

async def main_cli():
    print(Fore.CYAN + "🌍 Welcome to the AI Travel Designer!")
    print(Fore.CYAN + "Tell me what you like, and I'll design a dream trip for you.")
    print(Fore.YELLOW + "Type 'exit' to quit.\n")

    history: List[Dict[str, str]] = []
    agent = TravelAgent

    while True:
        user_input = input(Fore.GREEN + "👤 You: ")
        if user_input.lower() in ['exit', 'quit']:
            print(Fore.MAGENTA + "👋 Goodbye! Safe travels!")
            break

        history.append({"role": "user", "content": user_input})
        try:
            result = await Runner.run(agent, history, run_config=config)
            final = result.final_output

            agent_name = result.final_agent.name if hasattr(result, 'final_agent') and result.final_agent else "Assistant"
            print(Fore.BLUE + f"🤖 {agent_name}: " + Style.RESET_ALL + f"{final}")
            history.append({"role": "assistant", "content": final})

            if hasattr(result, 'final_agent') and result.final_agent and result.final_agent != agent:
                agent = result.final_agent
                print(Fore.LIGHTYELLOW_EX + f"🔁 Switched to {agent.name}\n")


        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main_cli())