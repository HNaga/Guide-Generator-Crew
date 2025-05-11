import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool, FileWriterTool

# SETUP ENV VARS
llm_model = os.getenv("GEMINI_MODEL")  # Example model, replace with actual model
llm_api_key = os.getenv("GEMINI_API_KEY")  # Ensure you have your API key set in the environment
llm = LLM(model=llm_model, 
          api_key= llm_api_key
         )

# TOOLS
search_tool = SerperDevTool()
file_writer = FileWriterTool()

# AGENTS

literature_scout = Agent(
    role="Expert Academic Search Specialist",
    goal="Identify 3-5 highly relevant academic papers on a given research topic",
    backstory=(
        "You are a top-tier literature researcher with access to scholarly databases."
        " You know how to identify impactful, peer-reviewed papers from reputable journals."
    ),
    tools=[search_tool],
    llm=llm,
    verbose=True,
    memory=True,
)

information_extractor = Agent(
    role="Detail-Oriented Research Analyst",
    goal="Carefully extract structured information from research papers",
    backstory=(
        "You're great at reading dense academic papers and pulling out exactly what's important:"
        " objectives, methods, findings, and conclusions."
    ),
    llm=llm,
    verbose=True,
    memory=True,
)

synthesis_writer = Agent(
    role="Lead Research Summarizer & Report Drafter",
    goal="Craft a clear, comprehensive 500-word summary of several academic papers",
    backstory=(
        "You are a scientific writer with a gift for clarity and insight."
        " You weave together multiple sources into a single coherent, analytical summary."
    ),
    tools=[file_writer],
    llm=llm,
    verbose=True,
    memory=True,
)

# TASKS

task_1 = Task(
    description=(
        "Search for 3-5 peer-reviewed academic papers published in the last 3 years on the topic:"
        " 'the impact of AI on climate change mitigation'."
        " Prioritize papers from major journals or conferences."
        "\nReturn a list with: Title, Authors, Year, and accessible URLs or DOIs."
    ),
    expected_output="A markdown list of 3-5 relevant academic papers with title, authors, year, and URL/DOI.",
    tools=[search_tool],
    agent=literature_scout,
)

task_2 = Task(
    description=(
        "You’ve received 3-5 paper references with URLs."
        " For each paper, extract the following:"
        "\n1. Main research question/objective"
        "\n2. Methodology used"
        "\n3. Key findings"
        "\n4. Main conclusion"
        "\n\nStructure each paper summary clearly and separately."
    ),
    expected_output="Structured summaries for each paper, labeled and separated clearly.",
    agent=information_extractor,
)

task_3 = Task(
    description=(
        "You have summaries of 3-5 academic papers on 'AI and climate change mitigation'."
        " Write a 500-word markdown report with:"
        "\n- Introduction to the topic"
        "\n- Collective summary of research goals"
        "\n- Comparison of findings (themes or divergent results)"
        "\n- A conclusion on what this research collectively implies"
        "\nSave the file as 'ai-climate-summary.md'"
    ),
    expected_output="A 500-word markdown report saved as 'ai-climate-summary.md'.",
    tools=[file_writer],
    agent=synthesis_writer,
)

# CREW
crew = Crew(
    agents=[literature_scout, information_extractor, synthesis_writer],
    tasks=[task_1, task_2, task_3],
    process=Process.sequential,
    verbose=True
)

# EXECUTE
if __name__ == "__main__":
    result = crew.kickoff()
    print("\n✅ Research summary completed!\n")
    print(result)
