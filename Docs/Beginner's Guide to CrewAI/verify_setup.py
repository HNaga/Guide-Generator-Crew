import os
from dotenv import load_dotenv # Used to load environment variables from a .env file

# Load environment variables from .env file.
# This should be one of the first things in your script if you use .env files.
load_dotenv()

print("--- Verifying CrewAI Setup ---")

# Check if the OpenAI API key is loaded
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    print("SUCCESS: OpenAI API Key found in environment variables.")
    # For verification, you might want to print a few characters, but be cautious:
    # print(f"Key starts with: {openai_api_key[:5]}... and ends with ...{openai_api_key[-4:]}")
else:
    print("WARNING: OpenAI API Key NOT found in environment variables.")
    print("Ensure it's set in your .env file (and loaded) or as a system environment variable.")
    print("Without an API key, agent execution requiring an LLM will fail.")

print("\n--- Checking CrewAI Library ---")
try:
    # Attempt to import core CrewAI components
    from crewai import Agent, Task, Crew, Process
    print("SUCCESS: CrewAI library imported successfully!")

    # Optional: Attempt a minimal agent instantiation if an API key is present.
    # This is a more thorough check as it tries to initialize the LLM interface.
    if openai_api_key:
        print("\n--- Attempting Basic Agent Instantiation (requires a valid API key) ---")
        # Note: This will attempt to initialize the default LLM, which is usually an OpenAI model.
        # If the API key is invalid, has insufficient credits, or there are network issues,
        # this step might raise an error.
        try:
            test_agent = Agent(
                role='Test Agent',
                goal='Verify CrewAI setup and connectivity to LLM.',
                backstory=(
                    "I am a simple agent created solely to verify that the "
                    "CrewAI installation is correct and that the connection "
                    "to the underlying Language Model (e.g., OpenAI) is functional."
                ),
                verbose=False, # Set to True for more detailed output during agent actions
                allow_delegation=False
                # By default, CrewAI will try to use OpenAI if an API key is found.
                # You can explicitly configure other LLMs later.
            )
            print("SUCCESS: Basic Agent instantiated successfully!")
            print("This indicates CrewAI can likely communicate with the LLM provider.")
        except Exception as e:
            print(f"ERROR instantiating Agent: {e}")
            print("This could be due to:")
            print("  - An invalid or expired API key.")
            print("  - Insufficient credits or billing issues with your LLM provider account.")
            print("  - Network connectivity problems.")
            print("  - Incorrect environment variable setup for the LLM provider.")
            print("Please double-check your API key and account status with the LLM provider.")
    else:
        print("\nSkipping basic agent instantiation test because OpenAI API Key was not found.")

except ImportError:
    print("ERROR: Failed to import CrewAI. Please check your installation.")
    print("Ensure you have run 'pip install crewai' in your activated virtual environment.")
except Exception as e:
    print(f"An unexpected error occurred during setup verification: {e}")

print("\n--- Verification Complete ---")