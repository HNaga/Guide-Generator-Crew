import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool, FileWriterTool

# ENVIRONMENT VARIABLES

llm_model = os.getenv("GEMINI_MODEL")  # Example model, replace with actual model
llm_api_key = os.getenv("GEMINI_API_KEY")  # Ensure you have your API key set in the environment
llm = LLM(model=llm_model, 
          api_key= llm_api_key
         )

# TOOLS
search_tool = SerperDevTool()
file_write_tool = FileWriterTool()

# AGENTS

trend_spotter = Agent(
    role="Senior Industry Analyst",
    goal="Identify 3-5 trending and credible articles in the field of AI from the past week",
    backstory=(
        "You're a veteran industry analyst with a sharp eye for what matters."
        " You scan trusted media outlets, research databases, and forums to uncover"
        " only the most impactful content shaping the field."
    ),
    tools=[search_tool],
    verbose=True,
    llm=llm,
    memory=True,
)

content_summarizer = Agent(
    role="Expert Technical Writer",
    goal="Summarize technical content clearly and engagingly for a general audience",
    backstory=(
        "With years of experience in technical journalism, you make complex ideas"
        " simple and interesting. Your goal is to make each summary punchy, clear,"
        " and informative."
    ),
    verbose=True,
    llm=llm,
    memory=True,
)

newsletter_editor = Agent(
    role="Chief Newsletter Editor",
    goal="Polish the newsletter into a cohesive, compelling piece ready for publishing",
    backstory=(
        "You've edited some of the most popular tech newsletters. Your skill lies"
        " in structuring information for readability and engagement."
    ),
    tools=[file_write_tool],
    verbose=True,
    llm=llm,
    memory=True,
)

# TASKS

task_1 = Task(
    description=(
        "Search and identify the 3-5 most relevant, credible, and trending articles"
        " published in the last 7 days about Artificial Intelligence. Include only articles"
        " that would be valuable for a tech-savvy audience."
        "\nReturn a list of article titles and URLs."
    ),
    expected_output="A bullet list of 3-5 article titles with their corresponding URLs.",
    agent=trend_spotter,
)

task_2 = Task(
    description=(
        "Given a list of article titles and URLs (from Task 1), read each article and write"
        " a concise ~150-word summary that highlights the core message and relevance."
        " Ensure clarity, insight, and a reader-friendly tone."
    ),
    expected_output="Summaries for each article, clearly separated and labeled.",
    agent=content_summarizer,
)

task_3 = Task(
    description=(
        "You are given multiple article summaries (from Task 2)."
        " Compile these into a cohesive newsletter in markdown format."
        " Write a 50-word introduction, smooth transitions between summaries,"
        " a 30-word conclusion, and suggest a catchy title for the newsletter."
        " Save the final output using FileWriteTool as 'ai-newsletter.md'."
    ),
    expected_output="A complete markdown-formatted newsletter file saved as 'ai-newsletter.md'.",
    agent=newsletter_editor,
    tools=[file_write_tool],
)

# CREW
crew = Crew(
    agents=[trend_spotter, content_summarizer, newsletter_editor],
    tasks=[task_1, task_2, task_3],
    process=Process.sequential,
    verbose=True
)

# EXECUTE
if __name__ == "__main__":
    result = crew.kickoff()
    print("\n✅ Newsletter generation complete!\n")
    print(result)
