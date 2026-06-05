# External
import enum
import re
import typing
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Dict, List
from sqlalchemy import Table, Column, MetaData, Text, DateTime, String
from sqlalchemy.dialects.postgresql import ARRAY

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


class SqlUniverseModel(BaseModel):
    """
    A custom base class that equips all child models with automated
    linguistic specification parsing capabilities for the search agent prompt.
    """

    @classmethod
    def to_sqlalchemy_table(cls, table_name: Universe, metadata: MetaData) -> Table:
        seen: set[str] = set()
        columns: list[Column] = []
        for field_name, field_info in cls.model_fields.items():
            col_name = re.sub(r"_(after|before)$", "", field_name)
            if col_name in seen:
                continue
            seen.add(col_name)
            columns.append(Column(col_name, cls._sql_type(field_info.annotation)))
        return Table(table_name.value, metadata, *columns)

    @classmethod
    def _sql_type(cls, annotation: type) -> object:
        if annotation is datetime:
            return DateTime(timezone=True)
        if isinstance(annotation, type) and issubclass(annotation, enum.Enum):
            return String()
        if typing.get_origin(annotation) is list:
            return ARRAY(String())
        return Text()


class UniverseModel(BaseModel):
    """
    Custom base class that equips all child models with automated
    linguistic specification parsing capabilities for the search agent prompt.
    """

    @classmethod
    def create_universe_definition_prompt(cls, universe_name: Universe) -> str:
        block = [f"Universe Name: {universe_name}. Description: {cls.__doc__.strip()} Fields:"]
        properties: dict = cls.model_json_schema().get("properties", {})

        for name, meta in properties.items():
            field_desc = meta.get("description", "No explicit field description declared.")
            field_type = meta.get("type", "string")
            field_role = "search"

            if "enum" in meta:
                choices = ", ".join([f"'{c}'" for c in meta["enum"]])
                field_type = f"Enum: [{choices}]"
                field_role = "filter"
            elif field_type == "array":
                items_type = meta.get("items", {}).get("type", "string")
                field_type = f"List of {items_type}s"
                field_role = "filter"
            elif meta.get("format") == "date-time":
                field_type = "string (ISO date-time format: YYYY-MM-DDTHH:MM:SS)"
                field_role = "filter"

            block.append(f"- {name} ({field_type}) [{field_role}]: {field_desc}")

        return "\n".join(block)


class UserMemories(UniverseModel, SqlUniverseModel):
    """A personalized timeline capturing individual user preferences, milestones, behavioral contexts, and historical user-agent interactions."""

    memory: str = Field(
        ...,
        description="The detailed content of the user memory, preference, or historical interaction context."
    )
    category: str = Field(
        ..., 
        description="The classification of the memory, e.g., 'preference', 'tool_usage', 'personal_bio', 'professional_milestone'."
    )
    emotional_salience: Priority = Field(
        ...,
        description="The emotional intensity or importance of the memory to the user, ranked as low, medium, or high."
    )
    created_at: datetime = Field(
        ...,
        description="Datetime when this memory was captured in ISO date format (YYYY-MM-DD)."
    )

    @classmethod
    def create_universe_definition_prompt(cls) -> str:
        return super().create_universe_definition_prompt(Universe.USER_MEMORIES)
    
    @classmethod
    def to_sqlalchemy_table(cls, metadata: MetaData) -> Table:
        return super().to_sqlalchemy_table(Universe.USER_MEMORIES, metadata)


class TeamProjects(UniverseModel, SqlUniverseModel):
    """An operational tracking ledger representing shared group work initiatives, delivery schedules, ownership, and project workspaces."""

    project_report: str = Field(
        ...,
        description="A comprehensive narrative of the project's current state, recent developments, or specific challenges faced."
    )
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

    @classmethod
    def to_sqlalchemy_table(cls, metadata: MetaData) -> Table:
        return super().to_sqlalchemy_table(Universe.TEAM_PROJECTS, metadata)


class OrganizationKnowledge(UniverseModel, SqlUniverseModel):
    """A comprehensive institutional repository housing authoritative corporate documentation, standard operating procedures, policies, and internal guides."""

    report: str = Field(
        ...,
        description="A detailed summary of the document's content, key points, or specific sections relevant to the search context."
    )
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

    @classmethod
    def create_universe_definition_prompt(cls) -> str:
        return super().create_universe_definition_prompt(Universe.ORGANIZATION_KNOWLEDGE)

    @classmethod
    def to_sqlalchemy_table(cls, metadata: MetaData) -> Table:
        return super().to_sqlalchemy_table(Universe.ORGANIZATION_KNOWLEDGE, metadata)


UNIVERSE_REGISTRY: dict[Universe, type[UniverseModel]] = {
    Universe.USER_MEMORIES: UserMemories,
    Universe.TEAM_PROJECTS: TeamProjects,
    Universe.ORGANIZATION_KNOWLEDGE: OrganizationKnowledge,
}