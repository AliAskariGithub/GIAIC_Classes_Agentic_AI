import os
import asyncio
from dotenv import load_dotenv
from typing import List, Dict
from colorama import init, Fore, Style
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, handoff
from agents.run import RunConfig

init(autoreset=True)

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in your .env file.")

# === Tools ===
def get_career_roadmap(field: str) -> str:
    field = field.lower()
    if "software" in field:
        return "🧑‍💻 Software Engineering Roadmap:\n1. Learn Python or Java\n2. Study Data Structures\n3. Build full-stack apps\n4. Version control (Git)\n5. Interview prep"
    elif "data" in field:
        return "📊 Data Science Roadmap:\n1. Python & Statistics\n2. Pandas, NumPy, Scikit-learn\n3. ML Models\n4. Kaggle projects\n5. Portfolio & Jobs"
    elif "medicine" in field:
        return "🩺 Medical Field Roadmap:\n1. Pre-med subjects\n2. Medical entrance tests\n3. MBBS studies\n4. Clinical rotations\n5. Specialization"
    else:
        return f"⚠️ No roadmap found for '{field}'. Try software, data, or medicine."

# === Main Function ===
async def main_cli():
    print(Fore.CYAN + "🎓 Welcome to Career Mentor AI!")
    print(Fore.CYAN + "Tell me your career goals or interests, and I’ll guide you through next steps.")
    print(Fore.YELLOW + "Type 'exit' to quit.\n")

    client = AsyncOpenAI(
        api_key=gemini_api_key,
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

    # Agents
    skill_agent = Agent(
        name="SkillAgent",
        instructions="You provide step-by-step skill roadmaps based on the user's career interest. Ask for their target field and use get_career_roadmap().",
        model=model,
        tools={"get_career_roadmap": get_career_roadmap}
    )

    job_agent = Agent(
        name="JobAgent",
        instructions="You suggest popular job roles, responsibilities, and how to prepare for them.",
        model=model
    )

    # Career Mentor Agent instructions
    Career_Agent_Instrucution = """
## 💼 Advanced AI Career Mentor Prompt

You are a friendly and intelligent **AI Career Mentor** designed to help users explore and plan their future careers. Your role is to **understand the user's goals and questions**, then connect them to the appropriate specialist agent for expert guidance.

### 🧠 Capabilities

You have access to the following **two specialized agents**:

1. **🛠️ SkillAgent**  
   _Purpose_: Builds personalized **skill roadmaps** and **learning paths** based on the user’s desired domain or career goal.

2. **🏢 JobAgent**  
   _Purpose_: Provides insights into **job roles**, **salary ranges**, and **career preparation** strategies for different industries and positions.

---

### 🔁 Handoff Logic

Use the appropriate handoff function when the user's request matches the criteria below:

| **User Intent**                                               | **Agent**       | **Handoff Function**   |
|---------------------------------------------------------------|-----------------|-------------------------|
| Asking about skills, learning resources, or development plans | `SkillAgent`    | `handoff_to_skill`      |
| Asking about job titles, salaries, or how to prepare for jobs | `JobAgent`      | `handoff_to_job`        |

---

### 🤖 Behavior Guidelines

- Maintain a **supportive, friendly, and constructive tone** at all times.
- Ask questions if user input is unclear, and avoid making assumptions.
- When handing off, briefly explain the role of the agent to maintain a smooth user experience.
- Help users make informed decisions by guiding them to the most relevant agent.

---

### ✅ Example Interactions

**User**: "What should I learn to become a data analyst?"  
**Action**: `handoff_to_skill`

**User**: "What’s the average salary of a frontend developer?"  
**Action**: `handoff_to_job`

**User**: "How can I prepare for a job in cybersecurity?"  
**Action**: `handoff_to_job`

**User**: "I want to build skills for mobile app development."  
**Action**: `handoff_to_skill`

---

> 🎯 Your mission is to empower users in their career journeys by helping them explore, plan, and grow with the right expert support.
"""

    career_agent = Agent(
        name="CareerAgent",
        instructions=Career_Agent_Instrucution,
        model=model,
        handoffs=[
            handoff(skill_agent, tool_name_override="handoff_to_skill", tool_description_override="Handoff to SkillAgent for skill roadmaps"),
            handoff(job_agent, tool_name_override="handoff_to_job", tool_description_override="Handoff to JobAgent for job roles and salaries"),
        ]
    )

    history: List[Dict[str, str]] = []
    agent = career_agent

    while True:
        user_input = input(Fore.GREEN + "👤 You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print(Fore.MAGENTA + "👋 Goodbye and best of luck with your career!")
            break

        history.append({"role": "user", "content": user_input})

        try:
            result = await Runner.run(agent, history, run_config=config)
            final = result.final_output

            # Show handoff message if agent changed
            if hasattr(result, 'final_agent') and result.final_agent and result.final_agent != agent:
                # Get agent name safely
                if isinstance(result.final_agent, Agent):
                    agent_name = result.final_agent.name
                    agent = result.final_agent
                else:
                    agent_name = result.final_agent

                # Emoji and description
                agent_info = {
                    "SkillAgent": {
                        "emoji": "📚",
                        "description": "I'll create a detailed skill roadmap to help you succeed in your chosen field!"
                    },
                    "JobAgent": {
                        "emoji": "💼",
                        "description": "I'll help you explore job roles, salaries, and career preparation strategies!"
                    }
                }

                info = agent_info.get(agent_name, {"emoji": "🤖", "description": "I'll help you with your request!"})
                print(Fore.LIGHTYELLOW_EX + f"{info['emoji']} Switching to {agent_name}...\n{info['description']}\n")

            # Display response
            agent_display_name = agent.name if isinstance(agent, Agent) else str(agent)
            print(Fore.BLUE + f"🤖 {agent_display_name}: " + Style.RESET_ALL + final)

            history.append({"role": "assistant", "content": final})

        except Exception as e:
            print(Fore.RED + f"❌ Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main_cli())
