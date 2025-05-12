import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import markdown
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from uuid import uuid4
llm_model = os.getenv("GEMINI_MODEL")  # Example model, replace with actual model
llm_api_key = os.getenv("GEMINI_API_KEY")  # Ensure you have your API key set in the environment
llm = LLM(model=llm_model, 
          api_key= llm_api_key
          )
# Custom Tool: Markdown Reader (unchanged)
@tool
def markdown_reader_tool(file_path: str) -> dict:
    """Reads a Markdown file and extracts headers and content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        html = markdown.markdown(content)
        sections = []
        current_section = {"header": "", "content": ""}
        for line in content.split('\n'):
            if line.startswith('#'):
                if current_section["header"] or current_section["content"]:
                    sections.append(current_section)
                current_section = {"header": line.strip('# ').strip(), "content": ""}
            else:
                current_section["content"] += line + "\n"
        if current_section["header"] or current_section["content"]:
            sections.append(current_section)
        return {"sections": sections, "raw_content": content}
    except Exception as e:
        return {"error": f"Failed to read Markdown file: {str(e)}"}

# Custom Tool: PowerPoint Generator (with validation)
@tool
def powerpoint_generator_tool(slides_data: list) -> str:
    """Generates a PowerPoint presentation from slide data."""
    try:
        # Validate input
        if not isinstance(slides_data, list):
            return f"Error: slides_data must be a list, got {type(slides_data)}"
        
        prs = Presentation()
        slide_layout = prs.slide_layouts[1]  # Title and Content layout
        for i, slide in enumerate(slides_data):
            # Ensure slide is a dictionary
            if not isinstance(slide, dict):
                return f"Error: Slide {i} is not a dictionary"

# Custom Tool: Image Log Generator (unchanged)
@tool
def image_log_tool(image_data: list) -> str:
    """Generates a Markdown log file with image requirements and prompts."""
    try:
        log_content = "# Image Log for Presentation\n\n"
        for item in image_data:
            log_content += f"## Slide: {item.get('slide_title', 'Untitled')}\n"
            log_content += f"- **Image Description**: {item.get('description', 'N/A')}\n"
            log_content += f"- **Prompt for Generation**: {item.get('prompt', 'N/A')}\n"
            log_content += f"- **Placeholder Path**: {item.get('placeholder_path', 'N/A')}\n\n"
        output_file = "image_log.md"
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(log_content)
        return f"Image log saved as {output_file}"
    except Exception as e:
        return f"Error generating image log: {str(e)}"

# Agents (unchanged)
content_reader = Agent(
    role="Content Reader",
    goal="Read and extract key sections from the Markdown course content file.",
    backstory="You are an expert in parsing and understanding Markdown documents, capable of extracting structured information efficiently.",
    tools=[markdown_reader_tool],
    llm=llm,
    verbose=True
)

content_analyzer = Agent(
    role="Content Analyzer",
    goal="Analyze the course content to identify key points and suggest visuals for a presentation.",
    backstory="You are a skilled analyst who can summarize complex content and recommend engaging visuals for presentations.",
    llm=llm,
    verbose=True
)

presentation_creator = Agent(
    role="Presentation Creator",
    goal="Generate a PowerPoint presentation based on analyzed content.",
    backstory="You are an expert in creating professional PowerPoint presentations using structured data.",
    tools=[powerpoint_generator_tool],
    llm=llm,
    verbose=True
)

image_logger = Agent(
    role="Image Logger",
    goal="Log image requirements and prompts for the presentation in a Markdown file.",
    backstory="You are meticulous in documenting visual requirements and crafting prompts for image generation.",
    tools=[image_log_tool],
    llm=llm,
    verbose=True
)

# Tasks
read_task = Task(
    description="Read the Markdown file 'output/CrewAI 101- Introduction to Autonomous AI Agents.md' and extract its sections and raw content.",
    expected_output="A dictionary containing a list of sections with headers and content, and the raw Markdown content.",
    agent=content_reader,
    tools=[markdown_reader_tool]
)

analyze_task = Task(
    description="Analyze the extracted Markdown content to identify key points for slides and suggest visuals (e.g., diagrams, illustrations) for each section. For each section, create a slide with a title (section header), summarized content (key points), and a suggested visual with a description and prompt for image generation.",
    expected_output="A list of dictionaries, each containing: 'title' (string, section header), 'content' (string, summarized key points), 'visual_description' (string, description of suggested visual), and 'visual_prompt' (string, prompt for image generation). Example: [{'title': 'Section 1', 'content': 'Summary...', 'visual_description': 'A diagram...', 'visual_prompt': 'Generate a diagram...'}]",
    agent=content_analyzer,
    context=[read_task]
)

presentation_task = Task(
    description="Create a PowerPoint presentation using the analyzed content, with one slide per section including title and key points. Use the 'title' and 'content' from each slide data dictionary.",
    expected_output="A confirmation message that the PowerPoint file 'presentation.pptx' has been created.",
    agent=presentation_creator,
    tools=[powerpoint_generator_tool],
    context=[analyze_task],
    output_file="presentation.pptx"
)

image_log_task = Task(
    description="Generate a Markdown log file listing the suggested visuals for each slide, including descriptions, prompts for image generation, and placeholder paths. Use the 'title', 'visual_description', and 'visual_prompt' from each slide data dictionary.",
    expected_output="A confirmation message that the image log file 'image_log.md' has been created.",
    agent=image_logger,
    tools=[image_log_tool],
    context=[analyze_task],
    output_file="image_log.md"
)

# Crew
crew = Crew(
    agents=[content_reader, content_analyzer, presentation_creator, image_logger],
    tasks=[read_task, analyze_task, presentation_task, image_log_task],
    process=Process.sequential,
    verbose=True
)

# Execute
if __name__ == "__main__":
    result = crew.kickoff()
    print(result)