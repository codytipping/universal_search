from sqlalchemy import MetaData, Table, select, and_, or_
from sqlalchemy.types import Text
from sqlalchemy.dialects import postgresql

from app.models import UniversalSearchPayload, UNIVERSE_REGISTRY
from app.logic import parse_logic_expression


def postgres_engine(payload: UniversalSearchPayload) -> str:
    model = UNIVERSE_REGISTRY[payload.target_table]
    table = model.to_sqlalchemy_table(MetaData())

    text_cols = [col for col in table.columns if isinstance(col.type, Text)]

    var_map = {
        var.id: or_(*(col.ilike(f"%{var.search_signal}%") for col in text_cols))
        for var in payload.search_variables
    }

    search_cond = parse_logic_expression(payload.logic_expression, var_map) if var_map else None
    filter_cond = _apply_metadata_filters(payload.metadata_filters, table)

    clauses = [c for c in (search_cond, filter_cond) if c is not None]
    stmt = select(table).where(and_(*clauses)) if clauses else select(table)

    return str(stmt.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))


def _apply_metadata_filters(filters: dict, table: Table):
    clauses = []
    for key, value in filters.items():
        col_name = key.removesuffix("_after").removesuffix("_before")
        col = table.c[col_name]
        if key.endswith("_after"):
            clauses.append(col >= value)
        elif key.endswith("_before"):
            clauses.append(col <= value)
        else:
            clauses.append(col == value)
    return and_(*clauses) if clauses else None
