# External
from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter
import os

# Internal
from app.prompts import create_system_prompt
from app.tools import universal_database_search


def create_universal_search_agent():
    """
    Initializes the Universal Search Agent with the specified system prompt and tool configuration.
    This agent is designed to translate natural language queries into structured search payloads for database querying.
    """
    return create_agent(
        model=ChatOpenRouter(model=os.getenv("OPENROUTER_MODEL"), temperature=0),
        tools=[universal_database_search],
        system_prompt=create_system_prompt(),
    )