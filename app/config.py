# Internal
from app.types import Universe
from app.models import UniverseModel, UserMemories, TeamProjects, OrganizationKnowledge


UNIVERSE_REGISTRY: dict[Universe, UniverseModel] = {
    Universe.USER_MEMORIES: UserMemories,
    Universe.TEAM_PROJECTS: TeamProjects,
    Universe.ORGANIZATION_KNOWLEDGE: OrganizationKnowledge,
}