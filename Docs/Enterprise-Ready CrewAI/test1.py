from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import logging # For structured logging

# Your CrewAI setup imports
# from .crew_factory import create_my_crew # Example: A function to instantiate your configured crew
from crewai import Crew, Process, Agent, Task # For direct setup example

# Configure logging (as covered in "Production-Grade Development")
logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') # Basic config


load_dotenv() # Load .env for local development; in prod, env vars are injected

app = FastAPI(
    title="CrewAI Enterprise Service",
    description="API for executing specialized CrewAI tasks.",
    version="1.0.0"
)

# Define request model using Pydantic for input validation
class CrewKickoffPayload(BaseModel):
    inputs: dict
    # Example: inputs: {"topic": "AI in renewable energy", "output_format": "detailed report"}

# --- This is a simplified setup for demonstration. ---
# In a real application, you'd load agent/task configs from YAMLs
# using your project's structure and instantiate them, possibly with factories.
def get_example_crew():
    # agent_factory = MyAgentFactory('src/agents.yaml')
    # task_factory = MyTaskFactory('src/tasks.yaml')
    # ... instantiate agents and tasks ...
    # For this example, a mock crew:
    mock_researcher = Agent(
        role="Mock Researcher",
        goal="Process input: {topic}",
        backstory="I am a mock researcher for API demonstration.",
        verbose=True,
        allow_delegation=False
    )
    mock_research_task = Task(
        description="Research the provided topic: {topic} and output in format: {output_format}.",
        expected_output="A brief summary based on the topic and output format.",
        agent=mock_researcher
    )
    # Note: Real task execution (especially LLM calls) is blocking if not handled asynchronously.
    return Crew(
        agents=[mock_researcher],
        tasks=[mock_research_task],
        process=Process.sequential,
        # memory=True, # If using memory, ensure backend (e.g., vector DB) is configured
        verbose=True # Adjust verbosity as needed
    )

# Global crew instance or initialized on startup (consider lifespan management for production)
# For simplicity, instantiated globally. In complex apps, manage via FastAPI's lifespan events or dependency injection.
# example_crew = get_example_crew()

# Using FastAPI's dependency injection for crew setup (better for testing and configuration)
async def get_crew_instance() -> Crew:
    # This function can be more complex, loading configs, initializing tools, etc.
    # This allows for easier mocking in tests.
    return get_example_crew() # For this example, returns a new instance each time. Cache if needed.

@app.post("/run-crew/")
async def run_crew_endpoint(
    payload: CrewKickoffPayload,
    background_tasks: BackgroundTasks, # For offloading tasks
    crew: Crew = Depends(get_crew_instance) # Inject crew instance
):
    """
    Kicks off the CrewAI crew with the provided inputs.
    For long-running crews, this endpoint should ideally enqueue a job
    and return a task ID for status polling.
    """
    try:
        logger.info(f"Received request to run crew with inputs: {payload.inputs}")

        # For truly non-blocking, long-running CrewAI tasks that are resource-intensive
        # or require persistence/retries, use a dedicated task queue (Celery, RQ).
        # The API would enqueue the job and return an immediate response (e.g., task ID).
        # Example: task_id = celery_app.send_task('execute_crew_task', args=[payload.inputs])
        #          return {"status": "processing_started", "task_id": task_id}

        # For simpler background tasks or if the crew execution is relatively fast:
        # result = crew.kickoff(inputs=payload.inputs) # Synchronous execution (can block)

        # Using BackgroundTasks for demonstration if results aren't immediately needed in response:
        # def crew_task_wrapper(inputs_dict):
        #     try:
        #         result = crew.kickoff(inputs=inputs_dict)
        #         logger.info(f"Crew execution completed. Result: {result}")
        #         # Store result somewhere (e.g., database, cache) if needed for later retrieval
        #     except Exception as e:
        #         logger.error(f"Error during background crew execution: {e}", exc_info=True)
        # background_tasks.add_task(crew_task_wrapper, payload.inputs)
        # return {"status": "processing_initiated", "message": "Crew execution started in background."}

        # For this example, let's assume a moderately fast synchronous execution:
        result = crew.kickoff(inputs=payload.inputs)
        logger.info(f"Crew execution successful. Result: {result}")
        return {"status": "success", "result": result}

    except Exception as e:
        logger.error(f"Error running crew: {e}", exc_info=True) # Detailed logging
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Health check endpoint
@app.get("/health", tags=["Management"])
async def health_check():
    return {"status": "healthy", "version": app.version}

# To run this FastAPI app (save as src/main.py):
# uvicorn src.main:app --reload --host 0.0.0.0 --port 8000