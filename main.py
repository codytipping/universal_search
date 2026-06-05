import json
import os
from datetime import datetime, timezone

from app.agents import create_universal_search_agent
from app.engines import postgres_engine
import app.tools as _tools

from langchain_core.messages import HumanMessage

from experiments.memories import CASES as MEMORY_CASES
from experiments.projects import CASES as PROJECT_CASES
from experiments.knowledge import CASES as KNOWLEDGE_CASES


RESULTS_DIR = "experiments/results"

SUITES = [
    ("User Memories", MEMORY_CASES),
    ("Team Projects", PROJECT_CASES),
    ("Organization Knowledge", KNOWLEDGE_CASES),
]


def run_experiments() -> None:
    agent = create_universal_search_agent()

    universe_results: dict[str, list] = {}

    for universe_name, cases in SUITES:
        suite = []
        for query, *_ in cases:
            _tools._payload_capture.clear()
            agent.invoke({"messages": HumanMessage(content=query)})

            llm_payload = _tools._payload_capture[-1] if _tools._payload_capture else None

            suite.append({
                "query": query,
                "payload": llm_payload.model_dump() if llm_payload else None,
                "sql": postgres_engine(llm_payload) if llm_payload else None,
            })

        universe_results[universe_name] = suite

    output = {
        "metadata": {
            "model": os.getenv("OPENROUTER_MODEL", "unknown"),
            "date": datetime.now(timezone.utc).isoformat(),
        },
        **universe_results,
    }

    os.makedirs(RESULTS_DIR, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path = os.path.join(RESULTS_DIR, f"results_{timestamp}.json")
    with open(path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {path}")


if __name__ == "__main__":
    run_experiments()