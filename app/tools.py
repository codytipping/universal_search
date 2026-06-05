# External
from langchain.tools import tool
from typing import Any, Dict, List

# Internal
from app.models import UniversalSearchPayload
from app.types import Universe
from app.engines import postgres_engine

_payload_capture: list[UniversalSearchPayload] = []


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
    payload = UniversalSearchPayload(
        target_table=target_table,
        search_variables=search_variables,
        logic_expression=logic_expression,
        metadata_filters=metadata_filters if metadata_filters else {},
    )

    _payload_capture.append(payload)
    engine = DATABASE_REGISTRY.get(target_table)
    return engine(payload)


DATABASE_REGISTRY = {
    Universe.USER_MEMORIES: postgres_engine,
    Universe.TEAM_PROJECTS: postgres_engine,
    Universe.ORGANIZATION_KNOWLEDGE: postgres_engine,
}