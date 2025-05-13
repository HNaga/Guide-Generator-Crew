import yaml
from pathlib import Path


class SlideTemplateRenderer:
    def __init__(self):
        template_path = Path("templates/slide_templates.yaml")
        if not template_path.exists():
            raise FileNotFoundError(f"Slide templates not found at {template_path}")

        with open(template_path, "r") as f:
            self.templates = yaml.safe_load(f)

    def render_title_slide(self, course_title: str, lecture_title: str, audience_level: str, slide_number: int):
        return self.templates["title_slide"].format(
            course_title=course_title,
            lecture_title=lecture_title,
            audience_level=audience_level,
            slide_number=slide_number
        )

    def render_code_slide(self, code_block: str, language: str = "python", slide_number: int = 1):
        return self.templates["code_slide"].format(
            code_block=code_block,
            slide_number=slide_number,
            language=language
        )

    def render_concept_slide(self, section_title: str, content: str, slide_number: int):
        return self.templates["concept_slide"].format(
            section_title=section_title,
            content=content,
            slide_number=slide_number
        )

    def render_summary_slide(self, summary_points: str, slide_number: int):
        return self.templates["summary_slide"].format(
            summary_points=summary_points,
            slide_number=slide_number
        )