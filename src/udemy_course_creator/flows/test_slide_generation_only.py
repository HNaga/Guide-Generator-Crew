import os
import json
from models.curriculum_model import CourseState, Curriculum
from flows.udemy_course_flow import UdemyCourseCreationFlow
from utils.helpers import sanitize_filename


def test_slides_only():
    print("🖼️ Testing Slide Generation from Saved Curriculum")

    # Load saved curriculum data
    curriculum_path = "output/curriculum/course_curriculum.json"
    if not os.path.exists(curriculum_path):
        raise FileNotFoundError(f"Curriculum JSON not found at {curriculum_path}")

    with open(curriculum_path, "r", encoding='utf-8') as f:
        curriculum_data = json.load(f)

    # Simulate state
    flow = UdemyCourseCreationFlow()

    flow._state = CourseState(
        course_title="Practical CrewAI: Output Mastery, Custom Tools & Workflow Design",
        course_subtitle="Master CrewAI by building real-world applications.",
        description_points=[
            "Learn how to design and implement CrewAI-based projects.",
            "Create complex agent workflows with custom tools."
        ],
        target_audience="Developers and AI enthusiasts familiar with Python who want to build advanced CrewAI-powered applications.",
        course_goal="By the end of this course, students will be able to design, implement, and deploy full-stack CrewAI applications.",
        curriculum=Curriculum(**curriculum_data)
    )

    print("📚 Loaded curriculum with:")
    for i, section in enumerate(flow.state.curriculum.sections, 1):
        print(f"   Section {i}: {section.title}")
        for j, lecture in enumerate(section.lectures, 1):
            print(f"      Lecture {j}: {lecture.title}")

    # Run only slide generation
    print("\n📐 Starting slide generation...")
    flow.generate_lecture_slides()
    flow.final_debug_report()
    print("✅ Test complete — slides generated!")


if __name__ == "__main__":
    test_slides_only()