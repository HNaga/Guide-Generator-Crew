from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from src.udemy_course_creator.config.llm_config import DEFAULT_LLM
llm = DEFAULT_LLM

@CrewBase
class ContentCrew:
    """Crew responsible for writing and reviewing lecture content"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_writer'],
            llm=llm
        )

    @agent
    def content_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_reviewer'],
            llm=llm
        )

    @task
    def write_lecture_content_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_lecture_content'],
            llm=llm
        )

    @task
    def review_lecture_content_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_lecture_content'],
            context=[self.write_lecture_content_task()],
            llm=llm
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )