# test_course_design_crew.py

from course_design_crew import CourseDesignCrew

def test_course_design():
    print("🧠 Testing Course Design Crew...")
    crew = CourseDesignCrew().crew()

    inputs = {
        "course_title": "Practical CrewAI: Output Mastery, Custom Tools & Workflow Design",
        "course_goal": "By the end of this course, students will be able to design, implement, and deploy full-stack CrewAI applications.",
        "target_audience": "Developers and AI enthusiasts familiar with Python who want to build advanced CrewAI-powered applications.",
        "description_points": """
            Learn how to design and implement CrewAI-based projects.
            Create complex agent workflows with custom tools.
            Understand memory management and feedback loops in CrewAI.
            Deploy your CrewAI app as a production-ready service.
        """
    }

    result = crew.kickoff(inputs=inputs)
    print("\n📝 Raw Curriculum Output:\n", result.raw)

if __name__ == "__main__":
    test_course_design()