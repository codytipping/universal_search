# Universal Search

This project creates the foundation for a universal search AI-tool that can be applied to any database.

### Current AI systems are faced with a complex problem:
```
A single user prompt may simultaneously reference many different object types, structured constraints, semantic similarity, contextual restrictions, and layered logical composition. 
```

### A robust solution must satisfy a stronger condition: 
```
Every admissible user prompt must correspond to a well-formed expression in a logically closed retrieval language with precisely defined semantics.
```

The Universal Search AI-tool satises this requirement. 

### The current challenges with most AI search systems:
1. Most AI search systems use many specialized search tools.
2. Search logic is often tightly coupled to specific data models, databases, or AI models.
3. Complex user requests usually require custom search code and procedural handling.
4. Many search systems cannot guarantee that every user request can be translated into a valid search expression.
5. Search logic, retrieval methods, ranking, and filtering are often mixed together, making systems harder to maintain and extend.

### The benefits of a single universal search tool:
1. A single search system allows any user request to be translated into one standard search expression, regardless of the underlying database.
2. A single search system can be heavily optimized for cost, latency, reliability, and accuracy because all search traffic flows through the same path.
3. The AI can focus on what it does best—translating natural language into deterministic logic—instead of choosing between many specialized tools.
4. New databases and data sources can be added by implementing a translator once, without changing how users search.
5. A single search system creates a consistent, predictable, and explainable search experience across all data types and domains.

## How AI was Used & Effectiveness

I primarily used Claude Code and Gemini. 

- AI was used throughout the project lifecycle: brainstorming the core concept, formulating design hypotheses, generating tests, and writing implementation code once the groundwork was established.
- AI excelled at generating experiments and test cases — given a clear schema and payload structure, it produced thorough, varied query coverage with minimal guidance.
- AI was highly effective at authoring the system prompt, tool definitions, and other descriptions.
- The key pattern that worked: establish the architecture, data models, and design contracts first, then delegate generation tasks to AI within that scaffolding.
- AI performed best as an accelerant on well-defined subtasks, not as an architect — directing it at a clearly scoped problem consistently produced clean, useful output.

## AI Failure-Points & Fixes

- Without explicit structure and instructions upfront, AI would generate overly complex solutions — multiple specialized tools, nested abstractions, and unnecessary indirection where a single clean design was needed.
- The fix was to dial back, restart with the correct structure defined in advance, and re-engage AI within those constraints rather than iterating on the wrong foundation.
- In some cases, the most effective correction was to write the initial scaffolding manually — once a concrete starting point existed, AI could extend it correctly rather than over-engineer from a blank slate.

## Future Work

- Expand engine support beyond PostgreSQL to other database types (ChromaDB, MongoDB, etc.) and external search sources such as Google Search.
- Formalize the experiment framework so generated payloads and SQL can be evaluated against golden-standard expected outputs.
- Enable cross-universe search — synthesizing results across multiple universes and database backends in a single query.
- Expand supported search types beyond keyword and semantic (e.g. hybrid search, BM25 ranking).
- Register each model column with its eligible search types (keyword, semantic, and/or hybrid) to enforce type-appropriate retrieval per field.
- Consolidate context filters into search types for a simpler, more unified query model.

## Project Limitations & Edges

- Semantic search currently falls back to ILIKE matching — it is not backed by real vector embeddings; this project establishes the baseline interface and payload contract, with true semantic retrieval as a future extension.
- Search operates within a single universe per query — cross-universe synthesis is not yet supported.
- The system generates SQL but does not execute against a live database; the engine layer compiles valid, inspectable queries but stops short of a real retrieval loop.
- Results are not ranked or scored — all matching rows are treated as equally relevant.
- The logic expression parser supports only five operators (AND, OR, NOT, XOR, IMPLIES); more complex retrieval logic requiring aggregation, subqueries, or fuzzy ranking is outside the current scope.