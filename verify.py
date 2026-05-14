"""Verify that the published rankings reproduce from the published data.

Reads ``events/*.json`` plus ``meta.json``, runs the engine, and asserts
the resulting ratings match ``current/rankings.json``.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import balloon_ranking_glicko as brg


def main() -> None:
    here = Path(__file__).parent
    meta = json.loads((here / "meta.json").read_text())
    params = meta["parameters"]
    engine = brg.RatingEngine(
        tau=params["tau"],
        initial_rating=params["initial_rating"],
        initial_rd=params["initial_rd"],
        initial_volatility=params["initial_volatility"],
    )

    events: list[brg.Event] = []
    for event_file in sorted((here / "events").glob("*.json")):
        doc = json.loads(event_file.read_text())
        tasks = []
        for task in doc["tasks"]:
            tasks.append(
                brg.Task(
                    task_id=task["task_id"],
                    results=tuple(
                        brg.TaskResult(
                            pilot_id=r["pilot_id"],
                            position=r["position"],
                            no_result=r["no_result"],
                        )
                        for r in task["results"]
                    ),
                )
            )
        events.append(
            brg.Event(
                event_id=doc["event_id"],
                event_date=date.fromisoformat(doc["event_date"]),
                tasks=tuple(tasks),
            )
        )

    ratings = engine.process_history(events)
    expected = json.loads((here / "current" / "rankings.json").read_text())

    for entry in expected:
        actual = ratings.get(entry["pilot_id"])
        assert actual is not None, f"missing pilot {entry['pilot_id']}"
        assert abs(actual.rating - entry["rating"]) < 1e-6, (
            f"rating mismatch for {entry['pilot_id']}: "
            f"expected {entry['rating']}, got {actual.rating}"
        )

    print(f"Verified {len(expected)} pilots against engine v{brg.__version__}.")


if __name__ == "__main__":
    main()
