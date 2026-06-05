from app.models import UniversalSearchPayload, SearchVariable


CASES: list[tuple[str, UniversalSearchPayload, str]] = [

    # 1. Single keyword, no filters
    (
        "Find all projects about mobile app.",
        UniversalSearchPayload(
            target_table="Team Projects",
            search_variables=[
                SearchVariable(id="v1", match_type="Keyword", search_signal="mobile app"),
            ],
            logic_expression="v1",
            metadata_filters={},
        ),
        'SELECT "Team Projects".project_report, "Team Projects".status, "Team Projects".priority, "Team Projects".owner_team, "Team Projects".lead_user_id, "Team Projects".target_quarter \n'
        'FROM "Team Projects" \n'
        'WHERE "Team Projects".project_report ILIKE \'%%mobile app%%\' OR "Team Projects".owner_team ILIKE \'%%mobile app%%\' OR "Team Projects".lead_user_id ILIKE \'%%mobile app%%\' OR "Team Projects".target_quarter ILIKE \'%%mobile app%%\'',
    ),

    # 2. Single keyword + one enum filter
    (
        "Find all in-progress projects about mobile app.",
        UniversalSearchPayload(
            target_table="Team Projects",
            search_variables=[
                SearchVariable(id="v1", match_type="Keyword", search_signal="mobile app"),
            ],
            logic_expression="v1",
            metadata_filters={"status": "in_progress"},
        ),
        'SELECT "Team Projects".project_report, "Team Projects".status, "Team Projects".priority, "Team Projects".owner_team, "Team Projects".lead_user_id, "Team Projects".target_quarter \n'
        'FROM "Team Projects" \n'
        'WHERE ("Team Projects".project_report ILIKE \'%%mobile app%%\' OR "Team Projects".owner_team ILIKE \'%%mobile app%%\' OR "Team Projects".lead_user_id ILIKE \'%%mobile app%%\' OR "Team Projects".target_quarter ILIKE \'%%mobile app%%\') AND "Team Projects".status = \'in_progress\'',
    ),

    # 3. Semantic search + two enum filters
    (
        "Find high priority in-progress projects about API development.",
        UniversalSearchPayload(
            target_table="Team Projects",
            search_variables=[
                SearchVariable(id="v1", match_type="Semantic", search_signal="API development"),
            ],
            logic_expression="v1",
            metadata_filters={"status": "in_progress", "priority": "high"},
        ),
        'SELECT "Team Projects".project_report, "Team Projects".status, "Team Projects".priority, "Team Projects".owner_team, "Team Projects".lead_user_id, "Team Projects".target_quarter \n'
        'FROM "Team Projects" \n'
        'WHERE ("Team Projects".project_report ILIKE \'%%API development%%\' OR "Team Projects".owner_team ILIKE \'%%API development%%\' OR "Team Projects".lead_user_id ILIKE \'%%API development%%\' OR "Team Projects".target_quarter ILIKE \'%%API development%%\') AND "Team Projects".status = \'in_progress\' AND "Team Projects".priority = \'high\'',
    ),

    # 4. AND of two keywords + two enum filters
    (
        "Find high priority in-progress projects covering both API and payment processing.",
        UniversalSearchPayload(
            target_table="Team Projects",
            search_variables=[
                SearchVariable(id="v1", match_type="Keyword", search_signal="API"),
                SearchVariable(id="v2", match_type="Keyword", search_signal="payment processing"),
            ],
            logic_expression="v1 AND v2",
            metadata_filters={"status": "in_progress", "priority": "high"},
        ),
        'SELECT "Team Projects".project_report, "Team Projects".status, "Team Projects".priority, "Team Projects".owner_team, "Team Projects".lead_user_id, "Team Projects".target_quarter \n'
        'FROM "Team Projects" \n'
        'WHERE ("Team Projects".project_report ILIKE \'%%API%%\' OR "Team Projects".owner_team ILIKE \'%%API%%\' OR "Team Projects".lead_user_id ILIKE \'%%API%%\' OR "Team Projects".target_quarter ILIKE \'%%API%%\') AND ("Team Projects".project_report ILIKE \'%%payment processing%%\' OR "Team Projects".owner_team ILIKE \'%%payment processing%%\' OR "Team Projects".lead_user_id ILIKE \'%%payment processing%%\' OR "Team Projects".target_quarter ILIKE \'%%payment processing%%\') AND "Team Projects".status = \'in_progress\' AND "Team Projects".priority = \'high\'',
    ),

    # 5. OR inside AND NOT + two metadata filters including text column
    (
        "Find high priority Q1-2026 projects about machine learning or data pipelines, but exclude anything focused on ETL migration.",
        UniversalSearchPayload(
            target_table="Team Projects",
            search_variables=[
                SearchVariable(id="v1", match_type="Semantic", search_signal="machine learning"),
                SearchVariable(id="v2", match_type="Semantic", search_signal="data pipelines"),
                SearchVariable(id="v3", match_type="Keyword", search_signal="ETL migration"),
            ],
            logic_expression="(v1 OR v2) AND NOT v3",
            metadata_filters={"target_quarter": "Q1-2026", "priority": "high"},
        ),
        'SELECT "Team Projects".project_report, "Team Projects".status, "Team Projects".priority, "Team Projects".owner_team, "Team Projects".lead_user_id, "Team Projects".target_quarter \n'
        'FROM "Team Projects" \n'
        'WHERE ("Team Projects".project_report ILIKE \'%%machine learning%%\' OR "Team Projects".owner_team ILIKE \'%%machine learning%%\' OR "Team Projects".lead_user_id ILIKE \'%%machine learning%%\' OR "Team Projects".target_quarter ILIKE \'%%machine learning%%\' OR "Team Projects".project_report ILIKE \'%%data pipelines%%\' OR "Team Projects".owner_team ILIKE \'%%data pipelines%%\' OR "Team Projects".lead_user_id ILIKE \'%%data pipelines%%\' OR "Team Projects".target_quarter ILIKE \'%%data pipelines%%\') AND NOT ("Team Projects".project_report ILIKE \'%%ETL migration%%\' OR "Team Projects".owner_team ILIKE \'%%ETL migration%%\' OR "Team Projects".lead_user_id ILIKE \'%%ETL migration%%\' OR "Team Projects".target_quarter ILIKE \'%%ETL migration%%\') AND "Team Projects".target_quarter = \'Q1-2026\' AND "Team Projects".priority = \'high\'',
    ),
]
