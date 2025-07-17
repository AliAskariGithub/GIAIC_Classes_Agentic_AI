#💼 Career Mentor Agent
"""
🧠 What It Does
Guide students through career exploration using multi-agent support:
    ● Recommends career paths based on interests
    ● Uses Tool: get_career_roadmap() to show skills needed for a chosen field
    ● Hands off between agents:
    ○ CareerAgent (suggests fields),
    ○ SkillAgent (shows skill-building plans),
    ○ JobAgent (shares real-world job roles)

⚙️ Uses:
    ● OpenAI Agent SDK + Runner
    ● Tools: Skill Roadmap Generator
    ● Handoff: Switch between Career, Skill, and Job Agents

🔔 Tools and Handoff have not been covered in class yet. You are encouraged to
explore these topics independently as part of this assignment. They will be explained
in an upcoming session to support your understanding"""


from dotenv import load_dotenv
load_dotenv()

# 🔧 Tool: Skill Roadmap Generator (simulated)
def get_career_roadmap(field: str) -> list[str]:
    """Simulate skill roadmap for a given career field."""
    roadmaps = {
        "Data Science": ["Python", "Statistics", "Machine Learning", "Data Visualization"],
        "Web Development": ["HTML", "CSS", "JavaScript", "React", "Backend APIs"],
        "AI": ["Python", "Deep Learning", "NLP", "TensorFlow", "Ethics"],
        "Cybersecurity": ["Networking", "Linux", "Penetration Testing", "Cryptography"],
    }
    return roadmaps.get(field, ["Research skills for this field online."])

# 🧠 CareerAgent: Accepts user input and returns career field
def career_agent() -> str:
    try:
        field = input("Enter your field of study or career: ")
        print(f"CareerAgent: You chose '{field}'.")
        return field
    except Exception as e:
        print(f"Error: {e}")
        return ""
    
# 📘 SkillAgent: Generates skill-building roadmap
def skills_agent(field: str) -> list[str]:
    try:
        print(f"SkillAgent: Generating skill roadmap for '{field}'...")
        skills = get_career_roadmap(field)
        print(f"SkillAgent: Recommended skills: {', '.join(skills)}")
        return skills
    except Exception as e:
        print(f"Error: {e}")
        return []

# 💼 JobAgent: Shares real-world job roles based on field
def job_agent(field: str) -> list[str]:
    try:
        job_title = input(f"Enter the job title you are interested in within '{field}': ")
        job_desc = f"Job description for {job_title} - https://www.indeed.com/q-{job_title.replace(' ', '-')}--jobs.html"
        print(f"JobAgent: Sharing job info for '{job_title}'.")
        return [job_desc]
    except Exception as e:
        print(f"Error: {e}")
        return []

# 🤖 Combined Agent: Simulates handoff between agents
def combined_agent() -> list[str]:
    try:
        # CareerAgent
        field = career_agent()
        if not field:
            return []
        # SkillAgent
        skills = skills_agent(field)
        # JobAgent
        job = job_agent(field)
        # Combine info
        info = [f"Career Field: {field}"]
        info += [f"Skill: {skill}" for skill in skills]
        info += job
        return info
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    result = combined_agent()
    for line in result:
        print(line)