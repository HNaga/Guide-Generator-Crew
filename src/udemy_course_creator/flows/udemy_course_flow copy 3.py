from crewai.flow.flow import Flow, start, listen
from models.curriculum_model import CourseState, Curriculum
#from typing import List, Dict
import os
import json
from crews.course_design_crew.course_design_crew import CourseDesignCrew
from crews.content_crew.content_crew import ContentCrew
from crews.asset_generation_crew.asset_generation_crew import AssetGenerationCrew
from tools.file_manager_tool import save_file
from utils.parser import parse_curriculum_markdown
from utils.helpers import sanitize_filename


class UdemyCourseCreationFlow(Flow[CourseState]):
    @start()
    def get_inputs(self):
        """Automatically receive inputs from main.py"""
        print("📥 Inputs received by flow.")
        return self.state

    @listen(get_inputs)
    def design_curriculum(self):
        print("🧠 Designing course curriculum...")
        crew = CourseDesignCrew().crew()

        result = crew.kickoff(inputs={
            "course_title": self.state.course_title,
            "course_goal": self.state.course_goal,
            "target_audience": self.state.target_audience,
            "description_points": "\n".join(self.state.description_points),
        })

        # Save raw output
        save_file("output/curriculum", "course_curriculum_raw.md", result.raw)

        # Extract structured data
        curriculum_data = self._extract_curriculum_data(result.raw)

        # Validate and store in flow state
        try:
            validated_curriculum = Curriculum(**curriculum_data)
            self.state.curriculum = validated_curriculum
            save_file("output/curriculum", "course_curriculum.json", json.dumps(curriculum_data, indent=2))
            print("✅ Curriculum validated and stored in structured format")
        except Exception as e:
            print(f"⚠️ Curriculum validation failed: {e}")
            self.state.curriculum = None

        print("✅ Curriculum designed and saved.")
        return self.state

    def _extract_curriculum_data(self, markdown_text: str) -> dict:
        """
        Try to extract JSON curriculum from LLM response.
        Fall back to Markdown parsing if needed.
        """
        print("🔍 Attempting to extract curriculum data...")
        print("Raw LLM Output:\n", markdown_text[:500] + "...")

        try:
            json_start = markdown_text.rfind("```json") + 6
            json_end = markdown_text.rfind("```", json_start)
            if json_start > 6 and json_end > json_start:
                json_str = markdown_text[json_start:json_end].strip()
                print("📄 Extracted JSON:\n", json_str)
                return json.loads(json_str)
            else:
                raise ValueError("No valid JSON block found")
        except Exception as e:
            print(f"⚠️ Failed to extract JSON: {e}")
            print("Parsing Markdown instead...")

        parsed = parse_curriculum_markdown(markdown_text)

        if not parsed["sections"]:
            raise ValueError("LLM did not return properly formatted curriculum")

        return parsed

    @listen(design_curriculum)
    def write_lecture_content(self):
        print("✍️ Writing lecture content...")

        if not self.state.curriculum:
            print("⚠️ No curriculum found. Skipping lecture writing.")
            return self.state

        for section in self.state.curriculum.sections:
            section_folder = sanitize_filename(section.title)
            section_dir = os.path.join("output", "lectures", section_folder)
            print(f"📁 Saving Section: {section.title} → {section_dir}")

            for lecture in section.lectures:
                print(f"📝 Generating lecture: {lecture.title}")
                crew = ContentCrew().crew()

                result = crew.kickoff(inputs={
                    "lecture_title": lecture.title,
                    "lecture_objective": lecture.objective,
                    "section_description": section.title,
                    "audience_level": self.state.target_audience,
                    "previous_sections": "No previous sections."  # Replace with real logic later
                })

                filename = f"{sanitize_filename(lecture.title)}.md"
                lecture_path = os.path.join(section_dir, filename)
                save_file(section_dir, filename, result.raw)
                print(f"💾 Lecture saved to: {lecture_path}")

        print("✅ Lecture content written and saved.")
        return self.state

    @listen(write_lecture_content)
    def generate_lecture_slides(self):
        print("🖼️ Generating lecture slides...")

        if not self.state.curriculum:
            print("⚠️ No curriculum data found. Skipping slide generation.")
            return self.state

        for section in self.state.curriculum.sections:
            section_folder = sanitize_filename(section.title)
            section_dir = os.path.join("output", "slides", section_folder)
            os.makedirs(section_dir, exist_ok=True)

            for lecture in section.lectures:
                lecture_title = lecture.title
                print(f"📐 Creating slides for: {lecture_title}")

                # Build correct lecture file path inside section folder
                lecture_filename = f"{sanitize_filename(lecture.title)}.md"
                lecture_path = os.path.join("output", "lectures", section_folder, lecture_filename)

                try:
                    with open(lecture_path, 'r', encoding='utf-8') as f:
                        lecture_content = f.read()
                    print(f"📄 Loaded lecture content from: {lecture_path}")
                except FileNotFoundError:
                    print(f"⚠️ Lecture file not found: {lecture_path}")
                    continue

                # Run slide generation crew
                crew = AssetGenerationCrew().crew()
                result = crew.kickoff(inputs={
                    "lecture_title": lecture.title,
                    "lecture_objective": lecture.objective,
                    "section_description": section.title,
                    "audience_level": self.state.target_audience,
                    "lecture_content": lecture_content
                })

                if not result.raw.strip():
                    raise ValueError(f"⚠️ Empty content returned for '{lecture.title}'")

                # Save slide content using sanitized name
                slide_filename = f"{sanitize_filename(lecture.title)}.md"
                save_file(section_dir, slide_filename, result.raw)
                print(f"💾 Slides saved to: {os.path.join(section_dir, slide_filename)}")

        print("✅ Slides generated and saved in structured format.")
        return self.state

    @listen(generate_lecture_slides)
    def final_debug_report(self):
        print("\n📊 Final Report:")
        if self.state.curriculum:
            total_lectures = sum(len(s.lectures) for s in self.state.curriculum.sections)
            print(f"Found {len(self.state.curriculum.sections)} sections")
            print(f"Found {total_lectures} lectures")
            print("Lectures written: output/lectures/<section>/<lecture>.md")
            print("Slides generated: output/slides/<section>/<lecture>.md")
        else:
            print("❌ Curriculum not available. Check earlier steps.")

        print("✅ Udemy course generation complete.")
        return self.state