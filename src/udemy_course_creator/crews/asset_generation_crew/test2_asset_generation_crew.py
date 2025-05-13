# test_generate_all_slides.py

import os
from asset_generation_crew import AssetGenerationCrew
from src.udemy_course_creator.utils.helpers import sanitize_filename
from src.udemy_course_creator.tools.file_manager_tool import save_file

def generate_slides_for_all_lectures():
    print("🖼️ Batch Slide Generation: Generating slides for all lectures")

    # Path to your lectures
    lectures_base_path = "output/lectures"
    slides_base_path = "output/slides"

    if not os.path.exists(lectures_base_path):
        print(f"❌ Lecture folder not found: {lectures_base_path}")
        return

    # Loop through each section folder
    for section_folder in os.listdir(lectures_base_path):
        section_path = os.path.join(lectures_base_path, section_folder)
        
        if not os.path.isdir(section_path):
            continue

        sanitized_section = sanitize_filename(section_folder)
        slide_section_dir = os.path.join(slides_base_path, sanitized_section)
        os.makedirs(slide_section_dir, exist_ok=True)

        print(f"\n📁 Processing Section: {section_folder}")

        # Loop through each lecture in the section
        for lecture_file in os.listdir(section_path):
            if not lecture_file.endswith(".md"):
                continue

            lecture_title = lecture_file.replace(".md", "").replace("_", " ")
            lecture_path = os.path.join(section_path, lecture_file)

            try:
                with open(lecture_path, 'r', encoding='utf-8') as f:
                    lecture_content = f.read()
            except Exception as e:
                print(f"⚠️ Failed to read {lecture_file}: {e}")
                continue

            print(f"📐 Generating slides for: {lecture_title}")

            crew = AssetGenerationCrew().crew()

            result = crew.kickoff(inputs={
                "lecture_title": lecture_title,
                "lecture_objective": f"Understand {lecture_title}",
                "section_description": section_folder.replace("_", " "),
                "audience_level": "intermediate",
                "lecture_content": lecture_content
            })

            if not result.raw.strip():
                print(f"⚠️ Empty slide content returned for '{lecture_title}'")
                continue

            # Save slide content
            slide_filename = lecture_file  # Same name or use a different one if needed
            slide_filepath = os.path.join(slide_section_dir, slide_filename)

            try:
                with open(slide_filepath, 'w', encoding='utf-8') as f:
                    f.write(result.raw)
                print(f"✅ Slides saved to: {slide_filepath}")
            except Exception as e:
                print(f"⚠️ Failed to save slide file: {e}")

    print("\n🎉 All slides generated successfully!")


if __name__ == "__main__":
    generate_slides_for_all_lectures()