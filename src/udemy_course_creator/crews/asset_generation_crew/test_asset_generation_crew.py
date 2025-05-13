# test_asset_generation_crew.py

import os
from asset_generation_crew import AssetGenerationCrew
from src.udemy_course_creator.utils.helpers import sanitize_filename
from src.udemy_course_creator.tools.file_manager_tool import save_file

def test_asset_generation_from_file(section_folder: str, lecture_file: str):
    print("🖼️ Testing Slide Generation from File")
    
    # Build paths
    lecture_path = os.path.join("output", "lectures", section_folder, lecture_file)
    
    if not os.path.exists(lecture_path):
        print(f"❌ Lecture file not found: {lecture_path}")
        return
    
    try:
        with open(lecture_path, 'r', encoding='utf-8') as f:
            lecture_content = f.read()
    except Exception as e:
        print(f"⚠️ Failed to read file: {e}")
        return

    print(f"📄 Loaded lecture content from: {lecture_path}")

    # Run crew
    crew = AssetGenerationCrew().crew()

    # Extract lecture title from filename (remove .md)
    lecture_title = lecture_file.replace(".md", "").replace("_", " ")

    result = crew.kickoff(inputs={
        "lecture_title": lecture_title,
        "lecture_objective": "Understand key concepts of CrewAI",
        "section_description": section_folder.replace("_", " "),
        "audience_level": "intermediate",
        "lecture_content": lecture_content
    })

    if not result.raw.strip():
        print("❌ Empty output returned from AssetGenerationCrew")
        return

    # Save slide content using sanitized name
    section_dir = os.path.join("output", "slides", sanitize_filename(section_folder))
    slide_filename = os.path.basename(lecture_file)  # Same name for now
    save_file(section_dir, slide_filename, result.raw)

    print(f"✅ Slides saved to: {os.path.join(section_dir, slide_filename)}")


if __name__ == "__main__":
    # Example usage:
    test_asset_generation_from_file(
        section_folder="Section_1_Introduction_to_CrewAI",
        lecture_file="1_What_is_CrewAI.md"
    )