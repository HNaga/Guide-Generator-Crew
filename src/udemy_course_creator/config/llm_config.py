# config/llm_config.py

from crewai import LLM
import os

DEFAULT_LLM = LLM(
    model="openai/gpt-4o-mini",  # ← Change this to switch models
    temperature=0.3,
    max_tokens=2048,
    api_key=os.getenv("OPENAI_API_KEY")  # Or Gemini, Anthropic, etc.
)

# Optional: Define other LLMs if needed
GEMINI_LLM = LLM(
    model="google/gemini-1.5-flash",
    temperature=0.2,
    max_tokens=2048,
    api_key=os.getenv("GEMINI_API_KEY")
)

ANTHROPIC_LLM = LLM(
    model="anthropic/claude-3-haiku",
    temperature=0.1,
    max_tokens=1024,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)