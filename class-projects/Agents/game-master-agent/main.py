# Game Master Agent (Fantasy Adventure Game)
"""
🧠 What It Does
Run a text-based adventure game using multiple AI agents:
    ● Narrates an adventure story based on player choices
    ● Uses Tool: roll_dice() and generate_event() to control game flow
    ● Hands off between:
    ○ NarratorAgent (story progress),
    ○ MonsterAgent (combat phase),
    ○ ItemAgent (inventory & rewards)

⚙️ Uses:
    ● OpenAI Agent SDK + Runner
    ● Tools: Dice Roller, Event Generator
    ● Handoff: Dynamic switches between roles based on gameplay

🔔Tools and Handoff have not been covered in class yet. You are encouraged to
explore these topics independently as part of this assignment. They will be explained
in an upcoming session to support your understanding."""

import random
import time

# ---------------- Tools ----------------

def roll_dice(sides=6) -> int:
    """Simulate a dice roll."""
    return random.randint(1, sides)

def generate_event() -> str:
    """Simulate a random fantasy event."""
    events = [
        "You enter a dark cave...",
        "You find a hidden chest!",
        "A monster appears!",
        "You meet a wandering trader.",
        "A trap is triggered!"
    ]
    return random.choice(events)

# ---------------- Agents ----------------

def narrator_agent() -> str:
    print("\n🎙️ NarratorAgent: Welcome to the Fantasy Adventure Game!")
    time.sleep(1)
    player_name = input("Enter your hero's name: ")
    print(f"\n🎙️ NarratorAgent: Brave {player_name}, your adventure begins...\n")
    time.sleep(1)

    event = generate_event()
    print(f"📜 Event: {event}")
    return event

def monster_agent() -> bool:
    print("\n👹 MonsterAgent: A wild monster appears! Prepare for battle!")
    time.sleep(1)
    player_roll = roll_dice()
    monster_roll = roll_dice()

    print(f"\n🎲 You rolled: {player_roll}")
    print(f"👾 Monster rolled: {monster_roll}")

    if player_roll >= monster_roll:
        print("✅ You defeated the monster!")
        return True
    else:
        print("💀 The monster defeated you. Game over.")
        return False

def item_agent(inventory: list):
    print("\n🎁 ItemAgent: Searching for loot...")
    items = ["Health Potion", "Magic Sword", "Gold Coins", "Armor", "Treasure Map"]
    found_item = random.choice(items)
    inventory.append(found_item)
    print(f"🧰 You received: {found_item}")

# ---------------- Game Flow Controller ----------------

def game_master():
    inventory = []

    while True:
        event = narrator_agent()

        if "monster" in event.lower():
            win = monster_agent()
            if not win:
                break
            item_agent(inventory)

        elif "chest" in event.lower() or "trap" in event.lower():
            item_agent(inventory)

        elif "trader" in event.lower():
            print("\n🧙 Trader offers you a rare item in exchange for 10 gold coins.")
            if "Gold Coins" in inventory:
                print("🤝 You traded 10 Gold Coins for a Magic Amulet!")
                inventory.remove("Gold Coins")
                inventory.append("Magic Amulet")
            else:
                print("💸 You don’t have any Gold Coins. You move on.")

        # Continue or Exit
        choice = input("\nDo you want to continue your adventure? (yes/no): ").strip().lower()
        if choice != "yes":
            break

    print("\n🎮 Game Over. Here's your final inventory:")
    print(f"🧾 {inventory}")

# ---------------- Run Game ----------------

if __name__ == "__main__":
    game_master()
