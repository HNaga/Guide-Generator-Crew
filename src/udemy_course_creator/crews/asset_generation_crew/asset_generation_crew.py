from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task

# Import centralized LLM
from config.llm_config import DEFAULT_LLM


@CrewBase
class AssetGenerationCrew:
    """Crew responsible for generating presentation slides and visual assets"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def slide_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['slide_generator'],
            llm=DEFAULT_LLM
        )

    @task
    def generate_lecture_slides_task(self) -> Task:
        return Task(config=self.tasks_config['generate_lecture_slides'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )