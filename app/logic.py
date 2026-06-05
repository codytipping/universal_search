# External
import re
from sqlalchemy import ColumnElement, and_, or_, not_

_TOKEN_RE = re.compile(r"\s*(AND|OR|NOT|XOR|IMPLIES|[vV]\d+|\(|\))\s*", re.IGNORECASE)
_KEYWORDS = {"AND", "OR", "NOT", "XOR", "IMPLIES"}


def parse_logic_expression(expression: str, var_map: dict[str, ColumnElement]) -> ColumnElement:
    return _Parser(_tokenize(expression), var_map).parse()


def _tokenize(expression: str) -> list[str]:
    tokens = []
    pos = 0
    while pos < len(expression):
        m = _TOKEN_RE.match(expression, pos)
        if not m:
            raise ValueError(f"Unexpected token near position {pos}: {expression[pos:pos+10]!r}")
        raw = m.group(1)
        tokens.append(raw.upper() if raw.upper() in _KEYWORDS else raw.lower())
        pos = m.end()
    return tokens


class _Parser:
    """Recursive descent parser. Operator precedence (lowest → highest): IMPLIES → OR → XOR → AND → NOT → atom"""

    def __init__(self, tokens: list[str], var_map: dict[str, ColumnElement]):
        self._tokens = tokens
        self._pos = 0
        self._var_map = var_map

    def _peek(self) -> str | None:
        return self._tokens[self._pos] if self._pos < len(self._tokens) else None

    def _consume(self, expected: str | None = None) -> str:
        token = self._tokens[self._pos]
        if expected and token != expected:
            raise ValueError(f"Expected {expected!r}, got {token!r}")
        self._pos += 1
        return token

    def parse(self) -> ColumnElement:
        expr = self._implies()
        if self._peek() is not None:
            raise ValueError(f"Unexpected trailing token: {self._peek()!r}")
        return expr

    def _implies(self) -> ColumnElement:
        left = self._or()
        if self._peek() == "IMPLIES":
            self._consume()
            return or_(not_(left), self._implies())
        return left

    def _or(self) -> ColumnElement:
        left = self._xor()
        while self._peek() == "OR":
            self._consume()
            left = or_(left, self._xor())
        return left

    def _xor(self) -> ColumnElement:
        left = self._and()
        while self._peek() == "XOR":
            self._consume()
            right = self._and()
            left = or_(and_(left, not_(right)), and_(not_(left), right))
        return left

    def _and(self) -> ColumnElement:
        left = self._not()
        while self._peek() == "AND":
            self._consume()
            left = and_(left, self._not())
        return left

    def _not(self) -> ColumnElement:
        if self._peek() == "NOT":
            self._consume()
            return not_(self._not())
        return self._atom()

    def _atom(self) -> ColumnElement:
        token = self._peek()
        if token == "(":
            self._consume()
            expr = self._implies()
            self._consume(")")
            return expr
        if token and re.fullmatch(r"v\d+", token):
            self._consume()
            if token not in self._var_map:
                raise ValueError(f"Variable {token!r} not in search_variables")
            return self._var_map[token]
        raise ValueError(f"Expected variable ID or '(', got {token!r}")