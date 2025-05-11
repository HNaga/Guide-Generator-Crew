import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, FileWriteTool

# ENVIRONMENT VARIABLES
os.environ["SERPER_API_KEY"] = "your-serper-api-key"
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# TOOLS
search_tool = SerperDevTool()
file_writer = FileWriteTool()

# AGENTS

preference_analyst = Agent(
    role="Client Intake Specialist & Travel Profiler",
    goal="Accurately extract and structure the user's trip preferences",
    backstory=(
        "You're an expert at translating a customer's vague travel ideas into a solid travel profile."
        " You listen well, summarize efficiently, and ensure planners have a crystal-clear brief."
    ),
    verbose=True,
    memory=True,
)

destination_expert = Agent(
    role="Local Guide & Activity Researcher",
    goal="Recommend diverse, exciting activities and restaurants tailored to traveler preferences",
    backstory=(
        "As a virtual Paris insider, you know everything from iconic landmarks to hidden gems."
        " Your job is to tailor the perfect mix of culture, history, and food based on interests and budget."
    ),
    tools=[search_tool],
    verbose=True,
    memory=True,
)

itinerary_coordinator = Agent(
    role="Master Itinerary Planner",
    goal="Craft a structured, fun, and realistic itinerary that balances exploration with rest",
    backstory=(
        "You're known for crafting perfect daily plans that feel like a breeze to follow."
        " You organize things by geography, opening hours, and flow."
    ),
    tools=[file_writer],
    verbose=True,
    memory=True,
)

# TASKS

task_1 = Task(
    description=(
        "A user wants to plan a 5-day trip to Paris. Their stated interests are: art museums,"
        " historical sites, and local cuisine. Their budget is 'moderate'."
        " Your task is to extract and clearly list the key preferences."
    ),
    expected_output="Destination: Paris\nDuration: 5 days\nInterests: Art Museums, Historical Sites, Local Cuisine\nBudget: Moderate",
    agent=preference_analyst,
)

task_2 = Task(
    description=(
        "Given the travel preferences (Destination: Paris, Duration: 5 days, Interests: Art Museums,"
        " Historical Sites, Local Cuisine, Budget: Moderate), find 2-3 activities and 2 dining"
        " options (1 casual, 1 upscale) per day."
        "\n\nEach suggestion must include a short description and practical details like cost or hours if possible."
    ),
    expected_output="Day-by-day plan with 2-3 activities and 2 restaurant options per day, each with a brief description.",
    agent=destination_expert,
)

task_3 = Task(
    description=(
        "Using the suggested daily activities and restaurants, structure a clear 5-day itinerary."
        " For each day, organize a morning, afternoon, and evening plan."
        " Include notes on travel time or booking needs if relevant."
        " Save the result as 'paris-itinerary.md'."
    ),
    expected_output="A markdown file 'paris-itinerary.md' containing a detailed 5-day itinerary with activities and meals organized by time of day.",
    agent=itinerary_coordinator,
    tools=[file_writer],
)

# CREW
crew = Crew(
    agents=[preference_analyst, destination_expert, itinerary_coordinator],
    tasks=[task_1, task_2, task_3],
    process=Process.sequential,
    verbose=True,
)

# EXECUTE
if __name__ == "__main__":
    result = crew.kickoff()
    print("\n✅ Trip itinerary created successfully!\n")
    print(result)
