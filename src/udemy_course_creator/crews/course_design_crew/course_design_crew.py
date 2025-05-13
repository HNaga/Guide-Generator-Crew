from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from src.udemy_course_creator.config.llm_config import DEFAULT_LLM
llm = DEFAULT_LLM

@CrewBase
class CourseDesignCrew:
    """Crew responsible for designing course curriculum"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def curriculum_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['curriculum_designer'],
            llm=llm,
            )

    @task
    def design_course_structure_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_course_structure'],
            llm=llm,
            )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    course_design_crew = CourseDesignCrew()
    course_design_crew.crew().kickoff()