#🧳 AI Travel Designer Agent
"""
🧠 What It Does
Plan a full travel experience by coordinating between specialized agents:
    ● Suggests destinations based on mood or interests
    ● Uses Tool: get_flights(), suggest_hotels() with mock data
    ● Hands off between:
    ○ DestinationAgent (finds places),
    ○ BookingAgent (simulates travel booking),
    ○ ExploreAgent (suggests attractions & food)

⚙️ Uses:
    ● OpenAI Agent SDK + Runner
    ● Tools: Travel Info Generator, Hotel Picker
    ● Handoff: Between Destination, Booking, and Explore Agents

🔔 Tools and Handoff have not been covered in class yet. You are encouraged to
explore these topics independently as part of this assignment. They will be explained
in an upcoming session to support your understanding."""

# 🧰 Tools (Simulated)
def get_flights(destination: str) -> list[str]:
    return [
        f"Flight 101 to {destination} - $300",
        f"Flight 202 to {destination} - $280",
        f"Flight 303 to {destination} - $320"
    ]

def suggest_hotels(destination: str) -> list[str]:
    return [
        f"{destination} Grand Hotel - 4 stars - $120/night",
        f"{destination} Budget Inn - 3 stars - $80/night",
        f"{destination} Luxury Suites - 5 stars - $200/night"
    ]

# 🎯 Destination Agent
def destination_agent() -> str:
    try:
        mood = input("Enter your travel mood (e.g., beach, mountains, culture): ").lower()
        destinations = {
            "beach": "Bali",
            "mountains": "Swiss Alps",
            "culture": "Kyoto",
            "adventure": "Queenstown",
            "romantic": "Paris"
        }
        destination = destinations.get(mood, "Generic City")
        print(f"DestinationAgent: Based on your mood '{mood}', we recommend: {destination}")
        return destination
    except Exception as e:
        print(f"Error: {e}")
        return ""

# 🏨 Booking Agent
def booking_agent(destination: str) -> list[str]:
    try:
        print(f"1 0Searching for flights and hotels in {destination}...")
        flights = get_flights(destination)
        hotels = suggest_hotels(destination)
        print("\n Flights:")
        for f in flights:
            print(" -", f)
        print("\n Hotels:")
        for h in hotels:
            print(" -", h)
        return flights + hotels
    except Exception as e:
        print(f"Error: {e}")
        return []

# 🍜 Explore Agent
def explore_agent(destination: str) -> list[str]:
    try:
        suggestions = {
            "Bali": ["Ubud Monkey Forest", "Beach Clubs", "Balinese Food"],
            "Swiss Alps": ["Skiing", "Mountain Hiking", "Swiss Chocolate"],
            "Kyoto": ["Fushimi Shrine", "Tea Ceremony", "Sushi Tasting"],
            "Queenstown": ["Bungee Jumping", "Lake Wakatipu", "Local BBQ"],
            "Paris": ["Eiffel Tower", "Louvre Museum", "French Pastries"],
            "Generic City": ["Museum Visit", "City Park", "Local Cuisine"]
        }
        explore_list = suggestions.get(destination, suggestions["Generic City"])
        print(f"\n ExploreAgent: Things to do in {destination}:")
        for item in explore_list:
            print(" -", item)
        return explore_list
    except Exception as e:
        print(f"Error: {e}")
        return []

# 🤖 AI Travel Designer Agent (handoff simulation)
def travel_designer_agent() -> list[str]:
    try:
        destination = destination_agent()
        if not destination:
            return []
        bookings = booking_agent(destination)
        explore = explore_agent(destination)
        
        final_plan = [f"📍 Destination: {destination}"] + \
                     [f"✈️ {f}" for f in bookings] + \
                     [f"🎒 To explore: {e}" for e in explore]
        return final_plan
    except Exception as e:
        print(f"Error: {e}")
        return []

# 🚀 Entry point
if __name__ == "__main__": 
    print("\n--- Your Travel Itinerary ---\n")
    travel_designer_agent()