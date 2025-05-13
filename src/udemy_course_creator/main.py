from flows.udemy_course_flow import UdemyCourseCreationFlow
#from flows.test_slide_generation_only import UdemyCourseCreationFlow
import sys
import io

# Ensure UTF-8 support in Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# ---------------------------
# Predefined Course Inputs
# ---------------------------
COURSE_TITLE = "Practical CrewAI: Output Mastery, Custom Tools & Workflow Design"
COURSE_SUBTITLE_IDEA = "Master CrewAI by building real-world applications and mastering advanced workflows."
COURSE_DESCRIPTION_POINTS = [
    "Learn how to design and implement CrewAI-based projects.",
    "Create complex agent workflows with custom tools.",
    "Understand memory management and feedback loops in CrewAI.",
    "Deploy your CrewAI app as a production-ready service."
]
TARGET_AUDIENCE_DESC = "Developers and AI enthusiasts familiar with Python who want to build advanced CrewAI-powered applications."
COURSE_MAIN_GOAL = "By the end of this course, students will be able to design, implement, and deploy full-stack CrewAI applications."

def kickoff():
    print("🚀 Starting Udemy Course Creation Flow...")
    flow = UdemyCourseCreationFlow()
    
    # Pass inputs directly instead of prompting
    flow.kickoff(inputs={
        "course_title": COURSE_TITLE,
        "course_subtitle": COURSE_SUBTITLE_IDEA,
        "description_points": COURSE_DESCRIPTION_POINTS,  # Pass as list, not joined string
        "target_audience": TARGET_AUDIENCE_DESC,
        "course_goal": COURSE_MAIN_GOAL
        })
    
    print("✅ Course generation complete!")

if __name__ == "__main__":
    kickoff()