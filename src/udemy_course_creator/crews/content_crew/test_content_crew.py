# test_content_crew.py

from content_crew import ContentCrew

def test_content_crew():
    print("✍️ Testing Content Writing Crew...")

    inputs = {
        "lecture_title": "What is CrewAI?",
        "lecture_objective": "Understand the basics of CrewAI.",
        "section_description": "Introduction to CrewAI",
        "audience_level": "intermediate",
        "previous_sections": "No previous sections."
    }

    crew = ContentCrew().crew()
    result = crew.kickoff(inputs=inputs)
    print("\n📄 Lecture Content Generated:\n", result.raw)

if __name__ == "__main__":
    test_content_crew()