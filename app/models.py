# External
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Dict, List

# Internal
from app.types import Priority, ProjectStatus, AccessLevel, Universe


class SearchVariable(BaseModel):
    """Schema for an isolated search criteria variable."""
    id: str = Field(
        ..., 
        description="Unique variable ID, e.g., 'v1', 'v2'.",
    )
    match_type: str = Field(
        ..., 
        description="Must be 'Keyword' (exact text) or 'Semantic' (vector meaning).",
    )
    search_signal: str = Field(
        ..., 
        description="The word phrase or concept to look for."
    )


class UniversalSearchPayload(BaseModel):
    """The multi-dimensional query payload for the Universal Search Agent."""
    target_table: str = Field(
        ..., 
        description="The database table name being searched (e.g., 'cases').",
    )
    search_variables: List[SearchVariable] = Field(
        ..., 
        description="Flat array of extracted text keywords or vector concepts.",
    )
    logic_expression: str = Field(
        ..., 
        description="A one-line boolean formula linking variable IDs (e.g., 'v1 AND NOT v2').",
    )
    metadata_filters: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Hard structural metadata filters (e.g., {'status': 'ACTIVE'}).",
    )


class UniverseModel(BaseModel):
    """
    Custom base class that equips all child models with automated
    linguistic specification parsing capabilities for the search agent prompt.
    """

    @classmethod
    def create_universe_definition_prompt(cls, universe_name: Universe) -> str:
        """
        Reflects over the specific child class calling this method and builds
        the precise string layout required by the search coordinator.
        """
        
        # Setup the precise header layout requested
        block = [f"Universe Name: {universe_name}. Description: {cls.__doc__.strip()} Fields:"]
        
        # Pull field properties via Pydantic reflection on the subclass (cls)
        properties: dict = cls.model_json_schema().get("properties", {})
        
        for name, meta in properties.items():
            field_desc = meta.get("description", "No explicit field description declared.")
            field_type = meta.get("type", "string")
            
            # Enrich type formatting context for complex sub-types
            if "enum" in meta:
                choices = ", ".join([f"'{c}'" for c in meta["enum"]])
                field_type = f"Enum: [{choices}]"
            elif field_type == "array":
                items_type = meta.get("items", {}).get("type", "string")
                field_type = f"List of {items_type}s"
            elif meta.get("format") == "date-time":
                field_type = "string (ISO date-time format: YYYY-MM-DDTHH:MM:SS)"
            
            # Add the precise markdown bullet point format
            block.append(f"- {name} ({field_type}): {field_desc}")
            
        return "\n".join(block)


class UserMemories(UniverseModel):
    """A personalized timeline capturing individual user preferences, milestones, behavioral contexts, and historical user-agent interactions."""

    category: str = Field(
        ..., 
        description="The classification of the memory, e.g., 'preference', 'tool_usage', 'personal_bio', 'professional_milestone'."
    )
    emotional_salience: Priority = Field(
        ...,
        description="The emotional intensity or importance of the memory to the user, ranked as low, medium, or high."
    )
    created_after: datetime = Field(
        ...,
        description="Filters for memories captured after this specific ISO date format (YYYY-MM-DD)."
    )
    created_before: datetime = Field(
        ...,
        description="Filters for memories captured before this specific ISO date format (YYYY-MM-DD)."
    )

    @classmethod
    def create_universe_definition_prompt(cls) -> str:
        return super().create_universe_definition_prompt(Universe.USER_MEMORIES)


class TeamProjects(UniverseModel):
    """An operational tracking ledger representing shared group work initiatives, delivery schedules, ownership, and project workspaces."""

    status: ProjectStatus = Field(
        ...,
        description="The exact current operational state of the target project."
    )
    priority: Priority = Field(
        ...,
        description="The execution urgency tier assigned to the project workspace."
    )
    owner_team: str = Field(
        ...,
        description="The name of the corporate department managing the project, e.g., 'Engineering', 'Marketing', 'Product'."
    )
    lead_user_id: str = Field(
        ...,
        description="The alphanumeric unique identifier of the designated project lead or manager."
    )
    target_quarter: str = Field(
        ...,
        description="The target delivery business quarter, e.g., 'Q1-2026', 'Q3-2026'."
    )

    @classmethod
    def create_universe_definition_prompt(cls) -> str:
        return super().create_universe_definition_prompt(Universe.TEAM_PROJECTS)


class OrganizationKnowledge(UniverseModel):
    """A comprehensive institutional repository housing authoritative corporate documentation, standard operating procedures, policies, and internal guides."""

    document_type: str = Field(
        ...,
        description="The nature of the knowledge base document, e.g., 'SOP', 'Architecture_RFC', 'HR_Policy', 'Onboarding_Guide'."
    )
    department: str = Field(
        ...,
        description="The operational unit this knowledge artifact belongs to, e.g., 'Legal', 'Security', 'DevOps', 'Finance'."
    )
    access_level: AccessLevel = Field(
        ...,
        description="The explicit compliance security clearance required to inspect the row data."
    )
    last_reviewed_after: datetime = Field(
        ...,
        description="Filters for documents that passed a governance compliance review after this date."
    )
    tags: List[str] = Field(
        ...,
        description="An array list of explicit, exact taxonomy string tags assigned to the document node."
    )

    @classmethod
    def create_universe_definition_prompt(cls) -> str:
        return super().create_universe_definition_prompt(Universe.ORGANIZATION_KNOWLEDGE)