# External
from enum import StrEnum


class Universe(StrEnum):
    """Defines the different 'universes' or contexts that the Universal Search Agent can operate within."""
    USER_MEMORIES = "User Memories"
    TEAM_PROJECTS = "Team Projects"
    ORGANIZATION_KNOWLEDGE = "Organization Knowledge"


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ProjectStatus(StrEnum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"


class AccessLevel(StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"