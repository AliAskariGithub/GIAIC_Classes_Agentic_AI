import os
import random
from dotenv import load_dotenv
from typing import cast
from colorama import init, Fore, Style
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, handoff
from agents.run import RunConfig

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
    model="gemini-2.5-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

# === Tool Functions ===
def roll_dice(sides: int = 20) -> int:
    return random.randint(1, sides)

def generate_event(context: str) -> str:
    events = {
        "forest": [
            "You hear rustling in the bushes. A goblin appears!",
            "You find an ancient tree with glowing runes.",
            "A traveling merchant offers you a mysterious potion."
        ],
        "dungeon": [
            "A trap triggers beneath your feet!",
            "A skeleton warrior blocks your path.",
            "You discover a chest filled with gold... or is it a mimic?"
        ],
        "village": [
            "A child runs up to you, asking for help.",
            "The blacksmith offers to upgrade your weapon.",
            "You overhear talk of a dragon nearby."
        ]
    }
    return random.choice(events.get(context.lower(), ["Nothing unusual happens..."]))

# === Agents ===
NarratorAgent = Agent(
    name="NarratorAgent",
    instructions="Narrate the fantasy adventure based on player decisions. Use vivid descriptions and advance the story.",
    model=model
)

MonsterAgent = Agent(
    name="MonsterAgent",
    instructions="Control monster behavior during combat. Ask the user what action they take (attack, defend, run), then narrate outcome using dice roll.",
    model=model,
    tools={"roll_dice": roll_dice}
)

ItemAgent = Agent(
    name="ItemAgent",
    instructions="Describe items found by the player and manage inventory. Assign rewards after events or combat.",
    model=model,
    tools={"generate_event": generate_event}
)

Game_Master_Agent_Instructions = """
## 🏰 Advanced Fantasy Adventure Game Master

You are a creative and engaging **Fantasy Adventure Game Master**, orchestrating an epic quest for the player. Your job is to **immerse the player in the adventure**, manage encounters, and guide them through thrilling challenges while delegating specialized tasks to the right agent.

### 🧠 Capabilities

You have access to the following **three specialized agents**:

1. **📜 NarratorAgent**  
   _Purpose_: Progresses the story, describes scenes, and narrates the unfolding adventure.

2. **🐉 MonsterAgent**  
   _Purpose_: Manages **combat encounters** using dice-based mechanics, enemy behaviors, and battle outcomes.

3. **💎 ItemAgent**  
   _Purpose_: Handles **inventory management**, distributing **rewards**, and managing **special items** during the quest.

---

### 🔁 Handoff Logic

Use the appropriate handoff function when the player's action matches the criteria below:

| **Player Intent**                                  | **Agent**         | **Handoff Function**     |
|----------------------------------------------------|-------------------|--------------------------|
| Exploring, moving, or progressing the story        | `NarratorAgent`   | `handoff_to_narrator`    |
| Initiating combat, attacking, or engaging enemies  | `MonsterAgent`    | `handoff_to_monster`     |
| Managing inventory, collecting items, or rewards   | `ItemAgent`       | `handoff_to_item`        |

---

### 🤖 Behavior Guidelines

- Keep the tone **immersive, descriptive, and engaging**.
- Maintain **consistent world-building** and continuity in the storyline.
- Always respond to player actions with logical consequences in the game world.
- When handing off, **smoothly transition** by narrating the context before passing to the specialized agent.

---

### ✅ Example Interactions

**Player**: "I walk through the ancient forest toward the glowing ruins."  
**Action**: `handoff_to_narrator`

**Player**: "I draw my sword and attack the goblin!"  
**Action**: `handoff_to_monster`

**Player**: "I check my bag for the healing potion."  
**Action**: `handoff_to_item`

**Player**: "After defeating the dragon, I search for treasure."  
**Action**: `handoff_to_item`

---

> 🎯 Your mission is to deliver an unforgettable fantasy adventure where every choice matters, every battle is thrilling, and every treasure feels earned.
"""

GameMasterAgent = Agent(
    name="GameMasterAgent",
    instructions=Game_Master_Agent_Instructions,
    model=model,
    handoffs=[
        handoff(NarratorAgent, tool_name_override="handoff_to_narrator"),
        handoff(MonsterAgent, tool_name_override="handoff_to_monster"),
        handoff(ItemAgent, tool_name_override="handoff_to_item"),
    ]
)

def main():
    print(Fore.MAGENTA + "🧙 Welcome, adventurer! Your quest begins now...")
    print(Fore.CYAN + "Tell me what you'd like to do — explore a forest, enter a dungeon, or visit a village?")

    history = []
    agent = NarratorAgent

    while True:
        user_input = input(Fore.GREEN + "👤 You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print(Fore.MAGENTA + "👋 Farewell, brave hero!")
            break

        history.append({"role": "user", "content": user_input})

        if any(word in user_input for word in ["attack", "defend", "monster", "fight", "battle", "combat", "enemy"]):
            new_agent = MonsterAgent
        elif any(word in user_input for word in ["item", "chest", "reward", "loot", "inventory", "collect", "treasure"]):
            new_agent = ItemAgent
        else:
            new_agent = NarratorAgent

        # === Agent Handoff Notification ===
        if new_agent != agent:
            agent_info = {
                "NarratorAgent": ("📖", "I'll narrate your adventure and guide you through the story!"),
                "MonsterAgent": ("⚔️", "I'll handle combat encounters and dice-based battles!"),
                "ItemAgent": ("🎁", "I'll manage your inventory and distribute rewards!")
            }
            emoji, desc = agent_info.get(new_agent.name, ("🤖", "I'll help you on your adventure!"))
            print(Fore.LIGHTYELLOW_EX + f"{emoji} Switching to {new_agent.name}...\n{desc}\n")
            agent = new_agent

        try:
            # === Manual Tool Execution for Quick Responses ===
            if agent == ItemAgent:
                for area in ["forest", "dungeon", "village"]:
                    if area in user_input:
                        event = generate_event(area)
                        print(Fore.CYAN + f"🎁 You discover:\n\n{event}")
                        history.append({"role": "assistant", "content": event})
                        break
                else:
                    result = Runner.run_sync(agent, history, run_config=cast(RunConfig, config))
                    print(Fore.BLUE + f"🤖 {agent.name}: {Style.RESET_ALL}{result.final_output}")
                    history.append({"role": "assistant", "content": result.final_output})

            elif agent == MonsterAgent:
                roll = roll_dice()
                outcome = "🗡️ Critical Hit!" if roll > 15 else "💢 Weak strike..." if roll < 5 else "⚔️ You strike the enemy."
                print(Fore.RED + f"You rolled a {roll}.\n{outcome}")
                history.append({"role": "assistant", "content": outcome})

            else:
                result = Runner.run_sync(agent, history, run_config=cast(RunConfig, config))
                print(Fore.BLUE + f"🤖 {agent.name}: {Style.RESET_ALL}{result.final_output}")
                history.append({"role": "assistant", "content": result.final_output})

        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}")

if __name__ == "__main__":
    main()