# 🧠 Multi-Agent AI Projects - README

Welcome to a collection of three exciting AI-powered multi-agent projects built using Python. These agents simulate real-world interactions and coordination between specialized roles. Each project focuses on a different domain: career guidance, travel planning, and fantasy gaming.

---

## 1. 🎓 Career Mentor Agent

### 📌 Description

This project helps students explore career paths using multiple agents that coordinate to recommend fields, skills, and jobs.

### 🔧 Functionalities

* **CareerAgent**: Suggests fields based on user interest.
* **SkillAgent**: Displays skill-building plans using a simulated tool `get_career_roadmap()`.
* **JobAgent**: Shows real-world job roles using mock job data.
* **CombinedAgent**: Simulates handoff between all agents for a smooth workflow.

### 🛠️ Tools & Technologies

* `get_career_roadmap()` (Simulated)
* Dynamic agent handoffs
* 📌 *OpenAI SDK / Tools*: 🚫 Not yet implemented (simulated only)

### ▶️ Run the Code

```bash
uv run main.py
```

---

## 2. ✈️ AI Travel Designer Agent

### 📌 Description

Plan a full travel experience based on mood or preferences by coordinating between travel-focused agents.

### 🔧 Functionalities

* **DestinationAgent**: Recommends places to visit.
* **BookingAgent**: Simulates booking of flights/hotels.
* **ExploreAgent**: Suggests food, activities, and attractions.
* **Tool Integration**: Uses mock versions of `get_flights()` and `suggest_hotels()`.

### 🛠️ Tools & Technologies

* Travel Info Generator (simulated)
* Hotel Picker (simulated)
* 📌 *OpenAI SDK / Tools*: 🚫 Not yet implemented (simulated only)

### ▶️ Run the Code

```bash
uv run main.py
```

---

## 3. 🕹️ Game Master Agent (Fantasy Adventure Game)

### 📌 Description

An interactive text-based adventure game where multiple AI agents control the game flow.

### 🔧 Functionalities

* **NarratorAgent**: Drives the story.
* **MonsterAgent**: Handles combat encounters using a `roll_dice()` tool.
* **ItemAgent**: Manages inventory and rewards.
* **GameMaster**: Oversees handoff between agents and maintains state.

### 🛠️ Tools & Technologies

* `roll_dice()` (Simulated)
* `generate_event()` (Simulated random fantasy events)
* Dynamic agent handoffs based on gameplay flow
* 📌 *OpenAI SDK / Tools*: 🚫 Not yet implemented (simulated only)

### ▶️ Run the Code

```bash
uv run main.py
```

---

## 📚 Learning Outcome

* Practice using agent-based architecture.
* Understand agent handoff design and simulate real-world workflows.
* Build mock tools in Python without relying on external APIs.

> ⚠️ **Note**: OpenAI tools and SDK integrations are simulated and not yet implemented. You are encouraged to explore those independently as an advanced extension.

---

## 📺 Recommended YouTube Resources

* [Intro to Multi-Agent Systems (AI)](https://www.youtube.com/watch?v=pZ1z1OjOKBQ)
* [Flask Web Apps Tutorial](https://www.youtube.com/watch?v=Z1RJmh_OqeA)
* [Build a Text-Based Game in Python](https://www.youtube.com/watch?v=DEcFCeFHz0I)
* [Career Roadmap Planning with Python](https://www.youtube.com/watch?v=sjG8yP4G8Ew)
* [Travel App Project with Python](https://www.youtube.com/watch?v=IEEhzQoKtQU)

---

Made with ❤️ by **Ali Askari**
