import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from langchain_openai import ChatOpenAI

# Load environment variables from .env file (especially OPENAI_API_KEY)
load_dotenv()

# Configure the Language Model (LLM)
# Ensure the model name is correct and you have API access.
llm = ChatOpenAI(model="gpt-4o-mini") # Example: "gpt-4o-mini" or "gpt-3.5-turbo"
llm_model = os.getenv("GEMINI_MODEL")  # Example model, replace with actual model
llm_api_key = os.getenv("GEMINI_API_KEY")  # Ensure you have your API key set in the environment
llm = LLM(model=llm_model, 
          api_key= llm_api_key
         )
# Agent 1: Idea Analyst
idea_analyst = Agent(
    role='Expert Idea Analyst for Blog Content',
    goal='Generate a concise outline with 3-4 key points for a blog post about the benefits of daily reading.',
    backstory=("You're a seasoned analyst renowned for distilling complex topics into clear, "
               "actionable blog post outlines. You focus on reader engagement and practical takeaways."),
    verbose=True,
    llm=llm,
    allow_delegation=False
)

# Agent 2: Content Writer
content_writer = Agent(
    role='Skilled Blog Post Writer',
    goal='Write a compelling and informative short blog post (approx. 200-300 words) based on a given outline.',
    backstory=("You're a creative writer who excels at transforming outlines into engaging blog posts. "
               "You have a knack for clear language and a friendly, informative tone."),
    verbose=True,
    llm=llm,
    allow_delegation=False
)

# Task 1: Generate blog post outline
outline_task = Task(
    description=("Create a blog post outline detailing 3-4 main benefits of incorporating daily reading "
                 "into one's routine. For each benefit, suggest a brief point or sub-topic."),
    expected_output=("A bullet-point outline for a blog post. It should include a catchy title suggestion "
                     "and 3-4 main benefit points, each with a brief elaboration (1 sentence)."),
    agent=idea_analyst
)

# Task 2: Write the blog post using the outline
writing_task = Task(
    description=("Using the provided blog post outline, write an engaging blog post of approximately 200-300 words. "
                 "Ensure the post flows well, expands on the outline points, and has a clear introduction and conclusion."),
    expected_output=("A complete blog post (200-300 words) in markdown format. It should include the title from the outline, "
                     "an introduction, body paragraphs developing each outline point, and a concluding paragraph."),
    agent=content_writer,
    context=[outline_task] # This task depends on the output of 'outline_task'
)

# Assemble the crew
reading_crew = Crew(
    agents=[idea_analyst, content_writer],
    tasks=[outline_task, writing_task],
    process=Process.sequential, # Tasks will be executed sequentially
    verbose=True # High verbosity for crew execution logging
)

# Kick off the crew's work
print("Crew kickoff! Starting the content creation process...")
result = reading_crew.kickoff()

print("\n\n----------------------------------------")
print("Crew execution finished! Final Output:")
print("----------------------------------------")
print(result)