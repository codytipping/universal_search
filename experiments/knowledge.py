from app.models import UniversalSearchPayload, SearchVariable


CASES: list[tuple[str, UniversalSearchPayload, str]] = [

    # 1. Single keyword, no filters
    (
        "Find documents about security policy.",
        UniversalSearchPayload(
            target_table="Organization Knowledge",
            search_variables=[
                SearchVariable(id="v1", match_type="Keyword", search_signal="security policy"),
            ],
            logic_expression="v1",
            metadata_filters={},
        ),
        'SELECT "Organization Knowledge".report, "Organization Knowledge".document_type, "Organization Knowledge".department, "Organization Knowledge".access_level \n'
        'FROM "Organization Knowledge" \n'
        'WHERE "Organization Knowledge".report ILIKE \'%%security policy%%\' OR "Organization Knowledge".document_type ILIKE \'%%security policy%%\' OR "Organization Knowledge".department ILIKE \'%%security policy%%\'',
    ),

    # 2. Single keyword + access level filter
    (
        "Find internal documents about security policy.",
        UniversalSearchPayload(
            target_table="Organization Knowledge",
            search_variables=[
                SearchVariable(id="v1", match_type="Keyword", search_signal="security policy"),
            ],
            logic_expression="v1",
            metadata_filters={"access_level": "internal"},
        ),
        'SELECT "Organization Knowledge".report, "Organization Knowledge".document_type, "Organization Knowledge".department, "Organization Knowledge".access_level \n'
        'FROM "Organization Knowledge" \n'
        'WHERE ("Organization Knowledge".report ILIKE \'%%security policy%%\' OR "Organization Knowledge".document_type ILIKE \'%%security policy%%\' OR "Organization Knowledge".department ILIKE \'%%security policy%%\') AND "Organization Knowledge".access_level = \'internal\'',
    ),

    # 3. Single keyword + two metadata filters (access level + department)
    (
        "Find public onboarding guides from the HR department.",
        UniversalSearchPayload(
            target_table="Organization Knowledge",
            search_variables=[
                SearchVariable(id="v1", match_type="Keyword", search_signal="onboarding"),
            ],
            logic_expression="v1",
            metadata_filters={"access_level": "public", "department": "HR"},
        ),
        'SELECT "Organization Knowledge".report, "Organization Knowledge".document_type, "Organization Knowledge".department, "Organization Knowledge".access_level \n'
        'FROM "Organization Knowledge" \n'
        'WHERE ("Organization Knowledge".report ILIKE \'%%onboarding%%\' OR "Organization Knowledge".document_type ILIKE \'%%onboarding%%\' OR "Organization Knowledge".department ILIKE \'%%onboarding%%\') AND "Organization Knowledge".access_level = \'public\' AND "Organization Knowledge".department = \'HR\'',
    ),

    # 4. AND NOT + access level filter
    (
        "Find internal security documents that aren't drafts.",
        UniversalSearchPayload(
            target_table="Organization Knowledge",
            search_variables=[
                SearchVariable(id="v1", match_type="Keyword", search_signal="security"),
                SearchVariable(id="v2", match_type="Keyword", search_signal="draft"),
            ],
            logic_expression="v1 AND NOT v2",
            metadata_filters={"access_level": "internal"},
        ),
        'SELECT "Organization Knowledge".report, "Organization Knowledge".document_type, "Organization Knowledge".department, "Organization Knowledge".access_level \n'
        'FROM "Organization Knowledge" \n'
        'WHERE ("Organization Knowledge".report ILIKE \'%%security%%\' OR "Organization Knowledge".document_type ILIKE \'%%security%%\' OR "Organization Knowledge".department ILIKE \'%%security%%\') AND NOT ("Organization Knowledge".report ILIKE \'%%draft%%\' OR "Organization Knowledge".document_type ILIKE \'%%draft%%\' OR "Organization Knowledge".department ILIKE \'%%draft%%\') AND "Organization Knowledge".access_level = \'internal\'',
    ),

    # 5. OR inside AND NOT + two metadata filters
    (
        "Find confidential DevOps documents about system architecture or compliance, but exclude anything mentioning legacy systems.",
        UniversalSearchPayload(
            target_table="Organization Knowledge",
            search_variables=[
                SearchVariable(id="v1", match_type="Semantic", search_signal="system architecture design"),
                SearchVariable(id="v2", match_type="Keyword", search_signal="compliance"),
                SearchVariable(id="v3", match_type="Keyword", search_signal="legacy systems"),
            ],
            logic_expression="(v1 OR v2) AND NOT v3",
            metadata_filters={"access_level": "confidential", "department": "DevOps"},
        ),
        'SELECT "Organization Knowledge".report, "Organization Knowledge".document_type, "Organization Knowledge".department, "Organization Knowledge".access_level \n'
        'FROM "Organization Knowledge" \n'
        'WHERE ("Organization Knowledge".report ILIKE \'%%system architecture design%%\' OR "Organization Knowledge".document_type ILIKE \'%%system architecture design%%\' OR "Organization Knowledge".department ILIKE \'%%system architecture design%%\' OR "Organization Knowledge".report ILIKE \'%%compliance%%\' OR "Organization Knowledge".document_type ILIKE \'%%compliance%%\' OR "Organization Knowledge".department ILIKE \'%%compliance%%\') AND NOT ("Organization Knowledge".report ILIKE \'%%legacy systems%%\' OR "Organization Knowledge".document_type ILIKE \'%%legacy systems%%\' OR "Organization Knowledge".department ILIKE \'%%legacy systems%%\') AND "Organization Knowledge".access_level = \'confidential\' AND "Organization Knowledge".department = \'DevOps\'',
    ),
]
