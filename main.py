# External
from langchain_core.messages import HumanMessage

# Internal
from app.agents import create_universal_search_agent


if __name__ == "__main__":

    # Init the agent
    agent = create_universal_search_agent()

    test_prompts: list[str] = [
        # Test Prompt 1: User Memories
        (
            "Find my high importance preferences or professional milestones captured "
            "between January 1st, 2025 and December 31st, 2025. Make sure the search "
            "focuses heavily on my preferred development tools and IDE setups, but "
            "completely exclude any old memories related to Python or Django frameworks."
        ),
        
        # Test Prompt 2: Team Projects
        (
            "Search through our active group workspaces for any Engineering or Product "
            "department projects scheduled for Q1-2026. The project must be currently "
            "marked as either 'in_progress' or 'planning', and it needs to mention our "
            "new database migration strategy or API schema redesign, but ensure it is "
            "not assigned to the lead user 'manager_alpha'."
        ),
        
        # Test Prompt 3: Organization Knowledge
        (
            "Locate internal standard operating procedures or architecture RFC documents "
            "within the Security and DevOps departments that have an explicit compliance "
            "clearance level of 'internal'. They must have been formally reviewed since "
            "June 2024, must be explicitly tagged with 'kubernetes' or 'aws', and if the "
            "document mentions zero-trust networking, it must also include our mandatory "
            "multi-factor authentication compliance mandate."
        )
    ]

    # Example execution loop for your LangChain test suite:
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- RUNNING TEST CASE {i} ---")
        response = agent.invoke({"messages": [HumanMessage(content=prompt)]})
        print(f"Response: {response}")