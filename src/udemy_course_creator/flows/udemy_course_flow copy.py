from crewai.flow.flow import Flow, listen, start

from tools.file_manager_tool import save_file
from crews.content_crew.content_crew import ContentCrew
from models.curriculum_model import CourseState #, Curriculum, Lecture, Section  

class UdemyCourseCreationFlow(Flow[CourseState]):
    @start()
    def get_inputs(self):
        """Automatically receive inputs from main.py"""
        return self.state

    @listen(get_inputs)
    def design_curriculum(self):
        print("🧠 Designing course curriculum...")
        from crews.course_design_crew.course_design_crew import CourseDesignCrew
        crew = CourseDesignCrew().crew()
        result = crew.kickoff(inputs={
            "course_title": self.state.course_title,
            "course_goal": self.state.course_goal,
            "target_audience": self.state.target_audience,
            "description_points": "\n".join(self.state.description_points),
        })

        # Save raw curriculum output
        from tools.file_manager_tool import save_file
        save_file("output/curriculum", "course_curriculum.md", result.raw)

        print("✅ Curriculum designed and saved.")
        return self.state
    

    @listen(design_curriculum)
    def write_lecture_content(self):
        print("✍️ Writing lecture content...")

        # Simulate parsing curriculum data
        curriculum_data = {
            "sections": [
                {
                    "title": "Introduction to CrewAI",
                    "lectures": [
                        {"title": "What is CrewAI?", "objective": "Understand basic concepts"},
                        {"title": "Core Components", "objective": "Learn about Agents, Tasks, and Crews"}
                    ]
                },
                {
                    "title": "Advanced CrewAI Techniques",
                    "lectures": [
                        {"title": "Custom Tools", "objective": "Build and integrate custom tools"},
                        {"title": "Memory Management", "objective": "Understand memory handling"}
                    ]
                }
            ]
        }

        for section in curriculum_data["sections"]:
            section_title = section["title"]
            section_path = f"output/lectures/{section_title.replace(' ', '_')}"

            for lecture in section["lectures"]:
                lecture_title = lecture["title"]
                lecture_objective = lecture["objective"]

                print(f"  ➤ Writing: {lecture_title}")

                crew = ContentCrew().crew()
                result = crew.kickoff(inputs={
                    "lecture_title": lecture_title,
                    "lecture_objective": lecture_objective,
                    "section_description": section_title,
                    "audience_level": self.state.target_audience,
                    "previous_sections": "No previous sections."  # Replace with real logic later
                })

                # Save lecture content
                filename = f"{lecture_title.replace(' ', '_')}.md"
                save_file(section_path, filename, result.raw)

        print("✅ Lecture content written and saved.")
        return self.state