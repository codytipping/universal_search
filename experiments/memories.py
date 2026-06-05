from app.models import UniversalSearchPayload, SearchVariable


CASES: list[tuple[str, UniversalSearchPayload, str]] = [

    # 1. Single keyword, no filters
    (
        "Show me my memories about Python.",
        UniversalSearchPayload(
            target_table="User Memories",
            search_variables=[
                SearchVariable(id="v1", match_type="Keyword", search_signal="python"),
            ],
            logic_expression="v1",
            metadata_filters={},
        ),
        'SELECT "User Memories".memory, "User Memories".category, "User Memories".emotional_salience, "User Memories".created_at \n'
        'FROM "User Memories" \n'
        'WHERE "User Memories".memory ILIKE \'%%python%%\' OR "User Memories".category ILIKE \'%%python%%\'',
    ),

    # 2. Single keyword + enum filter
    (
        "Find my high importance memories about Python.",
        UniversalSearchPayload(
            target_table="User Memories",
            search_variables=[
                SearchVariable(id="v1", match_type="Keyword", search_signal="python"),
            ],
            logic_expression="v1",
            metadata_filters={"emotional_salience": "high"},
        ),
        'SELECT "User Memories".memory, "User Memories".category, "User Memories".emotional_salience, "User Memories".created_at \n'
        'FROM "User Memories" \n'
        'WHERE ("User Memories".memory ILIKE \'%%python%%\' OR "User Memories".category ILIKE \'%%python%%\') AND "User Memories".emotional_salience = \'high\'',
    ),

    # 3. OR of two search variables, no filters
    (
        "Find memories about Python or machine learning.",
        UniversalSearchPayload(
            target_table="User Memories",
            search_variables=[
                SearchVariable(id="v1", match_type="Keyword", search_signal="python"),
                SearchVariable(id="v2", match_type="Semantic", search_signal="machine learning"),
            ],
            logic_expression="v1 OR v2",
            metadata_filters={},
        ),
        'SELECT "User Memories".memory, "User Memories".category, "User Memories".emotional_salience, "User Memories".created_at \n'
        'FROM "User Memories" \n'
        'WHERE "User Memories".memory ILIKE \'%%python%%\' OR "User Memories".category ILIKE \'%%python%%\' OR "User Memories".memory ILIKE \'%%machine learning%%\' OR "User Memories".category ILIKE \'%%machine learning%%\'',
    ),

    # 4. AND NOT + date range filter
    (
        "Find my personal biography memories that aren't about professional milestones, captured before 2025.",
        UniversalSearchPayload(
            target_table="User Memories",
            search_variables=[
                SearchVariable(id="v1", match_type="Semantic", search_signal="personal biography"),
                SearchVariable(id="v2", match_type="Keyword", search_signal="professional milestone"),
            ],
            logic_expression="v1 AND NOT v2",
            metadata_filters={"created_at_before": "2025-01-01T00:00:00"},
        ),
        'SELECT "User Memories".memory, "User Memories".category, "User Memories".emotional_salience, "User Memories".created_at \n'
        'FROM "User Memories" \n'
        'WHERE ("User Memories".memory ILIKE \'%%personal biography%%\' OR "User Memories".category ILIKE \'%%personal biography%%\') AND NOT ("User Memories".memory ILIKE \'%%professional milestone%%\' OR "User Memories".category ILIKE \'%%professional milestone%%\') AND "User Memories".created_at <= \'2025-01-01T00:00:00\'',
    ),

    # 5. OR inside AND NOT, two metadata filters
    (
        "Show me high importance memories about career achievements or programming that aren't related to hobbies, from before 2025.",
        UniversalSearchPayload(
            target_table="User Memories",
            search_variables=[
                SearchVariable(id="v1", match_type="Semantic", search_signal="career achievements"),
                SearchVariable(id="v2", match_type="Keyword", search_signal="programming"),
                SearchVariable(id="v3", match_type="Keyword", search_signal="hobbies"),
            ],
            logic_expression="(v1 OR v2) AND NOT v3",
            metadata_filters={"emotional_salience": "high", "created_at_before": "2025-01-01T00:00:00"},
        ),
        'SELECT "User Memories".memory, "User Memories".category, "User Memories".emotional_salience, "User Memories".created_at \n'
        'FROM "User Memories" \n'
        'WHERE ("User Memories".memory ILIKE \'%%career achievements%%\' OR "User Memories".category ILIKE \'%%career achievements%%\' OR "User Memories".memory ILIKE \'%%programming%%\' OR "User Memories".category ILIKE \'%%programming%%\') AND NOT ("User Memories".memory ILIKE \'%%hobbies%%\' OR "User Memories".category ILIKE \'%%hobbies%%\') AND "User Memories".emotional_salience = \'high\' AND "User Memories".created_at <= \'2025-01-01T00:00:00\'',
    ),
]