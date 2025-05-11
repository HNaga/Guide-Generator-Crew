# Guide Creator Flow

## Overview

Guide Creator Flow is a powerful tool built with CrewAI that automates the creation of comprehensive guides on any topic. This project leverages AI agents to generate well-structured, detailed guides tailored to specific audience levels (beginner, intermediate, or advanced).

The flow handles the entire guide creation process:
1. Collecting user input on the topic and target audience
2. Creating a structured outline
3. Generating detailed content for each section
4. Compiling everything into a complete guide

## Features

- Interactive command-line interface for guide creation
- Customizable topic and audience level targeting
- AI-powered content generation using CrewAI agents
- Structured output with proper formatting
- Support for various complexity levels (beginner to advanced)
- Automatic saving of guides in both Markdown and HTML formats

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [CrewAI](https://crewai.com) for orchestrating AI agents.

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd guide_creator_flow
   ```

2. Install the required dependencies:
   ```bash
   pip install -e .
   ```
   
   Alternatively, you can use the CrewAI CLI command:
   ```bash
   crewai install
   ```

3. Set up your environment variables for the LLM API keys in the `.env` file:
   ```
   # For OpenAI
   OPENAI_API_KEY=your_api_key_here
   
   # For Gemini (if using)
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=your_preferred_model
   ```

## Usage

### Running the Flow

To start the guide creation flow, run:

```bash
crewai run
```

This command initializes the guide_creator_flow as defined in your configuration.

### Interactive Process

The flow will guide you through these steps:

1. Enter the topic for your guide
2. Provide a detailed description of the topic (at least 50 characters)
3. Select your target audience level (beginner/intermediate/advanced)

The system will then:
- Generate a structured outline
- Create content for each section
- Compile the complete guide
- Save the output in both Markdown and HTML formats in the `output` directory

### Customizing Guide Creation

You can also programmatically create guides by importing and using the `kickoff` function:

```python
from guide_creator_flow.main import kickoff

kickoff(
    topic="Your Guide Topic",
    topic_details="Detailed description of what the guide should cover...",
    audience="beginner"  # or "intermediate" or "advanced"
)
```

See the `generate_course.py` file for an example implementation.

## Example Guides

The project includes several example guides in the `output` directory:

- Beginner's Guide to CrewAI
- Practical Projects with CrewAI
- Advanced CrewAI Orchestration
- CrewAI Agents with Vector Databases & RAG
- Enterprise-Ready CrewAI

## Project Structure

```
guide_creator_flow/
├── Docs/                  # Example documents and resources
├── output/                # Generated guides (MD and HTML)
├── src/
│   └── guide_creator_flow/
│       ├── crews/         # CrewAI crew definitions
│       ├── tools/         # Custom tools
│       ├── __init__.py
│       ├── generate_course.py  # Example script
│       └── main.py        # Main flow implementation
├── tests/                 # Test files
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

## Customizing

- Modify `src/guide_creator_flow/config/agents.yaml` to define your agents
- Modify `src/guide_creator_flow/config/tasks.yaml` to define your tasks
- Modify `src/guide_creator_flow/crew.py` to add your own logic, tools and specific args
- Modify `src/guide_creator_flow/main.py` to add custom inputs for your agents and tasks

## Support

For support, questions, or feedback regarding the Guide Creator Flow or CrewAI:

- Visit the [CrewAI documentation](https://docs.crewai.com)
- Reach out through the [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join the Discord community](https://discord.com/invite/X4JWnZnxPb)
- [Chat with the docs](https://chatg.pt/DWjSBZn)

Let's create comprehensive guides with the power of CrewAI!
