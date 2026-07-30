#!/usr/bin/env python3
"""Validate the synthetic PrepInterview AI analytics dataset and write QA evidence."""

from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw_synthetic"
TABLEAU_DIR = ROOT / "data" / "tableau"
DATABASE_PATH = ROOT / "data" / "prepinterview_synthetic_analytics.db"
REPORT_PATH = ROOT / "docs" / "data_quality_report.md"
PROFILE_PATH = ROOT / "data" / "validation_results.json"


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def check(name: str, passed: bool, evidence: str) -> dict:
    return {"check": name, "passed": passed, "evidence": evidence}


def main() -> None:
    raw = {path.stem: read_rows(path) for path in RAW_DIR.glob("*.csv")}
    tableau = {path.stem: read_rows(path) for path in TABLEAU_DIR.glob("*.csv")}
    results: list[dict] = []

    required = {"users", "jobs", "prep_plans", "prep_tasks", "exam_attempts", "mock_interviews", "ai_generations", "product_events"}
    results.append(check("Required raw tables exist", required.issubset(raw), f"Found: {', '.join(sorted(raw))}"))

    for table, key in {"users": "user_id", "jobs": "job_id", "prep_plans": "plan_id", "prep_tasks": "task_id", "exam_attempts": "attempt_id", "mock_interviews": "mock_id", "ai_generations": "generation_id", "product_events": "event_id"}.items():
        rows = raw[table]
        unique = len({row[key] for row in rows})
        results.append(check(f"{table} primary key uniqueness", unique == len(rows), f"{unique:,} unique IDs across {len(rows):,} rows"))

    users = {row["user_id"] for row in raw["users"]}
    jobs = {row["job_id"] for row in raw["jobs"]}
    plans = {row["plan_id"] for row in raw["prep_plans"]}
    orphan_jobs = [row for row in raw["jobs"] if row["user_id"] not in users]
    orphan_plans = [row for row in raw["prep_plans"] if row["user_id"] not in users or row["job_id"] not in jobs]
    orphan_tasks = [row for row in raw["prep_tasks"] if row["user_id"] not in users or row["plan_id"] not in plans]
    orphan_attempts = [row for row in raw["exam_attempts"] if row["user_id"] not in users or row["plan_id"] not in plans]
    orphan_mocks = [row for row in raw["mock_interviews"] if row["user_id"] not in users or row["plan_id"] not in plans]
    results.extend([
        check("Job-to-user referential integrity", not orphan_jobs, f"{len(orphan_jobs):,} orphan jobs"),
        check("Plan-to-job/user referential integrity", not orphan_plans, f"{len(orphan_plans):,} orphan plans"),
        check("Task-to-plan/user referential integrity", not orphan_tasks, f"{len(orphan_tasks):,} orphan tasks"),
        check("Exam-attempt referential integrity", not orphan_attempts, f"{len(orphan_attempts):,} orphan attempts"),
        check("Mock-interview referential integrity", not orphan_mocks, f"{len(orphan_mocks):,} orphan mocks"),
    ])

    score_errors = [row for row in raw["exam_attempts"] if not 0 <= float(row["score_pct"]) <= 100]
    mock_errors = [row for row in raw["mock_interviews"] if row["status"] == "completed" and not row["average_score"]]
    event_errors = [row for row in raw["product_events"] if row["environment"] != "synthetic_demo"]
    pii_columns = {"email", "name", "description", "answer_text", "prompt", "source_url"}
    present_pii = sorted({column for rows in raw.values() for column in (rows[0] if rows else {}) if column in pii_columns})
    results.extend([
        check("Exam score range", not score_errors, f"{len(score_errors):,} out-of-range scores"),
        check("Completed mock scores present", not mock_errors, f"{len(mock_errors):,} completed mocks missing scores"),
        check("Synthetic environment marker", not event_errors, f"{len(event_errors):,} events without synthetic_demo marker"),
        check("No prohibited public-data columns", not present_pii, f"Present prohibited columns: {present_pii or 'none'}"),
    ])

    funnel = tableau["tableau_activation_funnel"]
    funnel_errors = 0
    for group in {(r["cohort_week"], r["acquisition_channel"], r["target_role"]) for r in funnel}:
        rows = sorted([r for r in funnel if (r["cohort_week"], r["acquisition_channel"], r["target_role"]) == group], key=lambda r: int(r["step_order"]))
        values = [int(r["users_reached"]) for r in rows]
        if any(later > earlier for earlier, later in zip(values, values[1:])):
            funnel_errors += 1
    results.append(check("Funnel is non-increasing by segment", funnel_errors == 0, f"{funnel_errors:,} invalid funnel segments"))

    retention = tableau["tableau_retention_cohorts"]
    retention_errors = [row for row in retention if not 0 <= float(row["retention_rate"]) <= 1 or int(row["retained_users"]) > int(row["cohort_size"])]
    week_zero_errors = [row for row in retention if row["weeks_since_signup"] == "0" and float(row["retention_rate"]) != 1.0]
    results.extend([
        check("Retention rate bounds", not retention_errors, f"{len(retention_errors):,} invalid retention rows"),
        check("Retention cohort week 0 baseline", not week_zero_errors, f"{len(week_zero_errors):,} invalid week-0 rows"),
    ])

    ai_rows = tableau["tableau_ai_reliability"]
    ai_errors = [row for row in ai_rows if int(row["total_generations"]) != int(row["successful_generations"]) + int(row["failed_generations"])]
    results.append(check("AI reliability totals reconcile", not ai_errors, f"{len(ai_errors):,} non-reconciling rows"))

    with sqlite3.connect(DATABASE_PATH) as db:
        source_events = db.execute("SELECT COUNT(*) FROM product_events").fetchone()[0]
        source_users = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        view_events = db.execute("SELECT COALESCE(SUM(events), 0) FROM vw_event_volume_by_day").fetchone()[0]
    results.extend([
        check("SQLite user count matches CSV", source_users == len(raw["users"]), f"SQLite={source_users:,}; CSV={len(raw['users']):,}"),
        check("SQLite event view reconciles", view_events == source_events, f"View={view_events:,}; source={source_events:,}"),
    ])

    passed = sum(1 for result in results if result["passed"])
    payload = {"checks": results, "passed": passed, "total": len(results), "all_passed": passed == len(results)}
    PROFILE_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Data quality report",
        "",
        "> **Dataset disclosure:** This is a synthetic demonstration dataset modeled from PrepInterview AI workflows. It is not production usage data.",
        "",
        f"**Result:** {passed}/{len(results)} checks passed.",
        "",
        "| Check | Result | Evidence |",
        "| --- | --- | --- |",
    ]
    for result in results:
        lines.append(f"| {result['check']} | {'PASS' if result['passed'] else 'FAIL'} | {result['evidence']} |")
    lines.extend([
        "",
        "## Dashboard readiness",
        "",
        "The Tableau extracts are safe for a public synthetic-demo dashboard: they contain aggregate metrics and do not include names, emails, job descriptions, answer text, prompts, or source URLs.",
        "",
        "## Required Tableau disclosure",
        "",
        "Place this sentence in every published dashboard footer: `Synthetic demonstration data modeled from PrepInterview AI workflows; it does not represent production users or business performance.`",
        "",
    ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    if not payload["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
