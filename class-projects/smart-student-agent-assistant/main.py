import datetime
import json
from typing import Dict, List

#Schedular Agent
def schedular_agent(topics: list[str], deadline: str) -> List[Dict]:
    try:
        deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")
    
    today = datetime.date.today()
    days_remaining = (deadline_date - today).days
    if days_remaining <= 0:
        raise ValueError("The deadline must be a future date.")

    study_days = max(1, days_remaining // len(topics)) 
    study_plan = []
    current_day = today

    for topic in topics:
        end_day = current_day + datetime.timedelta(days=study_days - 1)
        study_plan.append({
            "topic": topic,
            "start_date": str(current_day),
            "end_date": str(end_day)
        })
        current_day = end_day + datetime.timedelta(days=1)
        return study_plan
    
#Research Agent
def research_agent(topic: str) -> list[str]:
    return [ 
        f"What is {topic}? - https://www.wikipedia.org/wiki{topic.replace(' ', '_')}",
        f"Youtube Intro to {topic} - https://www.youtube.com/results?search_query=introduction+to+{topic.replace(' ', '+')}",
        f"Benefits and Risks of {topic} - https://medium.com/tag/{topic.replace(' ', '-')}",
        f"Research papers on {topic} - https://scholar.google.com/scholar?q={topic.replace(' ', '+')}",
    ]

#Summarizer Agent
def summarizer_agent(snippets: List[str]) -> str:
    return " | ".join(snippets)

def run_study_assistant():
    topics_input = input("Enter the study topics , separated by commas: ")
    deadline = input("Enter the deadline (YYYY-MM-DD): ")
    topics = [t.strip() for t in topics_input.split(",") if t.strip()]

    if not topics:
        print("No valid topics provided.")
        return
    
    try:
        study_plan = schedular_agent(topics, deadline)
    except Exception as e:
        print(f"Error : {e}")
        return
    full_output = []

    for item in study_plan:
        topics = item["topic"]
        print(f"Researching {topics}...")
        research = research_agent(topics)
        summary = summarizer_agent(research)

        item_output = {
            "topic": item["topic"],
            "start_date": item["start_date"],
            "end_date": item["end_date"],
            "summary": summary
        }
        full_output.append(item_output)
        print(f"Summary for {topics} : \n {summary}")

        with open("study_assistant_output.json", "w") as f:
            json.dump(full_output, f, indent=4)
            print("\n study plan and summaries as saved in your study_assistant_output.json file")

if __name__ == "__main__":
    run_study_assistant()