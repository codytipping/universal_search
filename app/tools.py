# External
from langchain.tools import tool
from typing import Any, Dict, List

# Internal
from app.models import UniversalSearchPayload


# Temporary
import json


@tool("universal_database_search", args_schema=UniversalSearchPayload)
def universal_database_search(
    target_table: str,
    logic_expression: str,
    search_variables: List[Dict[str, Any]],
    metadata_filters: Dict[str, Any],
) -> str:
    """
    Executes a unified keyword, semantic, and metadata search over a target database table.
    Use this tool whenever a user requests to search, find, or filter information objects.
    """
    
    # Safely convert Pydantic SearchVariable objects into standard dictionaries
    serialized_variables = []
    for var in search_variables:
        # Check if it's a Pydantic v2 object
        if hasattr(var, "model_dump"):
            serialized_variables.append(var.model_dump())
        # Check if it's a Pydantic v1 object
        elif hasattr(var, "dict"):
            serialized_variables.append(var.dict())
        # If it's already a standard dictionary, leave it alone
        else:
            serialized_variables.append(var)

    # Group the structured parameters passed by the LLM agent
    raw_payload = {
        "target_table": target_table,
        "metadata_filters": metadata_filters if metadata_filters else {},
        "search_variables": serialized_variables,
        "logic_expression": logic_expression
    }
    
    # Format the payload into an easily inspectable, indented JSON string
    pretty_json = json.dumps(raw_payload, indent=4)
    
    # Print directly to the backend terminal server console for immediate validation
    print("\n[DEBUG] RECEIVED STRUCTURAL SEARCH PAYLOAD FROM AGENT:")
    print(pretty_json)
    print("-" * 60)
    
    # Return a status report string back to the agent's internal chain memory
    return f"SUCCESS: Payload received and verified.\n\n```json\n{pretty_json}\n```"