#!/usr/bin/env python3
"""Create a reproducible, explicitly synthetic analytics dataset for PrepInterview AI.

This script intentionally models the application's real workflow without using
production data, names, emails, job descriptions, answer text, or API content.
It is for a portfolio analytics prototype only, never a claim about live usage.
"""

from __future__ import annotations

import csv
import json
import random
import shutil
import sqlite3
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw_synthetic"
TABLEAU_DIR = ROOT / "data" / "tableau"
DATABASE_PATH = ROOT / "data" / "prepinterview_synthetic_analytics.db"
PROFILE_PATH = ROOT / "data" / "data_profile.json"
SEED = 20260728
START_DATE = date(2026, 1, 1)
END_DATE = date(2026, 6, 30)
USER_COUNT = 8000

ROLE_TOPICS = {
    "Software Engineer": ["Algorithms", "System Design", "APIs", "Databases", "Behavioral"],
    "Data Analyst": ["SQL", "Statistics", "Tableau", "Business Metrics", "Behavioral"],
    "Product Manager": ["Product Sense", "Metrics", "Execution", "Strategy", "Behavioral"],
    "UX Designer": ["Portfolio", "Research", "Design Critique", "Collaboration", "Behavioral"],
    "Finance Analyst": ["Financial Modeling", "Excel", "Forecasting", "Accounting", "Behavioral"],
}
CHANNELS = ["LinkedIn extension", "Handshake extension", "Company career site", "Manual paste"]
CHANNEL_WEIGHTS = [0.34, 0.24, 0.18, 0.24]
CHANNEL_BEHAVIOR = {
    "LinkedIn extension": {"login": 0.92, "job": 0.70, "plan": 0.67, "note": 0.74, "exam": 0.68, "mock": 0.48},
    "Handshake extension": {"login": 0.94, "job": 0.76, "plan": 0.71, "note": 0.78, "exam": 0.72, "mock": 0.52},
    "Company career site": {"login": 0.89, "job": 0.62, "plan": 0.61, "note": 0.69, "exam": 0.63, "mock": 0.43},
    "Manual paste": {"login": 0.86, "job": 0.58, "plan": 0.56, "note": 0.64, "exam": 0.57, "mock": 0.37},
}
TASK_TYPES = ["study", "study", "study", "exam", "coding", "mock_interview", "revision"]
DIFFICULTIES = ["Easy", "Medium", "Hard"]


def iso(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


def monday(value: date) -> str:
    return (value - timedelta(days=value.weekday())).isoformat()


def bounded_datetime(rng: random.Random, start: datetime, end: datetime) -> datetime:
    if end <= start:
        return start
    seconds = int((end - start).total_seconds())
    return start + timedelta(seconds=rng.randint(0, seconds))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to create an empty dataset: {path.name}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def mean(values: list[float]) -> float:
    return round(sum(values) / len(values), 2) if values else 0.0


def build_dataset() -> dict[str, list[dict]]:
    rng = random.Random(SEED)
    users: list[dict] = []
    jobs: list[dict] = []
    prep_plans: list[dict] = []
    prep_tasks: list[dict] = []
    exam_attempts: list[dict] = []
    mock_interviews: list[dict] = []
    ai_generations: list[dict] = []
    product_events: list[dict] = []
    state: dict[str, dict] = {}
    ids = Counter()

    def next_id(prefix: str) -> str:
        ids[prefix] += 1
        return f"syn_{prefix}_{ids[prefix]:07d}"

    def add_event(
        user_id: str,
        when: datetime,
        event_name: str,
        feature: str,
        *,
        target_role: str,
        channel: str,
        job_id: str = "",
        plan_id: str = "",
    ) -> None:
        product_events.append({
            "event_id": next_id("evt"),
            "user_id": user_id,
            "session_id": next_id("ses"),
            "occurred_at": iso(when),
            "event_name": event_name,
            "feature": feature,
            "job_id": job_id,
            "plan_id": plan_id,
            "target_role": target_role,
            "acquisition_channel": channel,
            "environment": "synthetic_demo",
        })

    def add_generation(user_id: str, when: datetime, feature: str, target_role: str) -> bool:
        success = rng.random() < (0.952 if feature != "mock_interview" else 0.938)
        latency = max(380, int(rng.gauss(2150 if feature == "study_notes" else 1650, 540)))
        input_tokens = max(210, int(rng.gauss(820, 190)))
        output_tokens = max(120, int(rng.gauss(1050 if feature == "study_notes" else 670, 220))) if success else 0
        ai_generations.append({
            "generation_id": next_id("gen"),
            "user_id": user_id,
            "occurred_at": iso(when),
            "feature": feature,
            "status": "success" if success else "failure",
            "provider": "OpenAI" if success else "OpenAI",
            "model": "synthetic-model-reference",
            "latency_ms": latency,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "target_role": target_role,
        })
        return success

    start_dt = datetime.combine(START_DATE, datetime.min.time())
    end_dt = datetime.combine(END_DATE, datetime.max.time())

    for index in range(1, USER_COUNT + 1):
        user_id = f"syn_user_{index:06d}"
        signup = bounded_datetime(rng, start_dt, end_dt - timedelta(days=7))
        channel = rng.choices(CHANNELS, weights=CHANNEL_WEIGHTS, k=1)[0]
        role = rng.choice(list(ROLE_TOPICS))
        experience = rng.choices(["Student", "Early career", "Career switcher"], weights=[0.34, 0.46, 0.20], k=1)[0]
        users.append({
            "user_id": user_id,
            "signup_at": iso(signup),
            "cohort_week": monday(signup.date()),
            "acquisition_channel": channel,
            "target_role": role,
            "experience_level": experience,
            "environment": "synthetic_demo",
        })
        info = {"signup": signup, "channel": channel, "role": role, "jobs": [], "plans": [], "steps": {"Account created": True}}
        state[user_id] = info
        add_event(user_id, signup, "account_created", "auth", target_role=role, channel=channel)

        behavior = CHANNEL_BEHAVIOR[channel]
        if rng.random() >= behavior["login"]:
            continue
        login_at = signup + timedelta(minutes=rng.randint(1, 720))
        add_event(user_id, login_at, "login_completed", "auth", target_role=role, channel=channel)
        info["steps"]["Logged in"] = True

        if rng.random() >= behavior["job"]:
            continue
        job_count = 1 if rng.random() < 0.73 else rng.choice([2, 3])
        for _ in range(job_count):
            job_at = login_at + timedelta(days=rng.randint(0, 16), minutes=rng.randint(5, 620))
            if job_at > end_dt:
                continue
            job_id = next_id("job")
            source_type = "URL capture" if "extension" in channel or channel == "Company career site" else "Manual description"
            jobs.append({
                "job_id": job_id,
                "user_id": user_id,
                "created_at": iso(job_at),
                "source_type": source_type,
                "acquisition_channel": channel,
                "target_role": role,
                "interview_window_days": rng.randint(7, 28),
                "environment": "synthetic_demo",
            })
            info["jobs"].append(job_id)
            add_event(user_id, job_at, "job_saved", "jobs", target_role=role, channel=channel, job_id=job_id)
            info["steps"]["Job saved"] = True
            analysis_at = job_at + timedelta(minutes=rng.randint(1, 14))
            analysis_success = add_generation(user_id, analysis_at, "job_analysis", role)
            if analysis_success:
                add_event(user_id, analysis_at, "job_analysis_completed", "jobs", target_role=role, channel=channel, job_id=job_id)

            if rng.random() >= behavior["plan"]:
                continue
            plan_at = job_at + timedelta(hours=rng.randint(1, 72))
            if plan_at > end_dt:
                continue
            plan_id = next_id("plan")
            days_until = rng.randint(7, 21)
            task_count = rng.randint(7, 16)
            plan_success = add_generation(user_id, plan_at, "prep_plan", role)
            prep_plans.append({
                "plan_id": plan_id,
                "job_id": job_id,
                "user_id": user_id,
                "generated_at": iso(plan_at),
                "days_until_interview": days_until,
                "planned_task_count": task_count,
                "generation_status": "success" if plan_success else "fallback_or_retry",
                "target_role": role,
                "acquisition_channel": channel,
                "environment": "synthetic_demo",
            })
            info["plans"].append(plan_id)
            add_event(user_id, plan_at, "prep_plan_generated", "prep_plans", target_role=role, channel=channel, job_id=job_id, plan_id=plan_id)
            info["steps"]["Prep plan generated"] = True

            completed_study = False
            submitted_exam = False
            for task_number in range(1, task_count + 1):
                scheduled = plan_at + timedelta(days=min(task_number - 1, days_until - 1), hours=rng.randint(7, 21))
                if scheduled > end_dt:
                    scheduled = end_dt - timedelta(hours=rng.randint(1, 8))
                task_type = rng.choice(TASK_TYPES)
                topic = rng.choice(ROLE_TOPICS[role])
                completion_probability = behavior["note"] if task_type in {"study", "revision", "coding"} else behavior["exam"] if task_type == "exam" else behavior["mock"]
                is_complete = rng.random() < completion_probability
                completed_at = scheduled + timedelta(minutes=rng.randint(18, 150)) if is_complete else None
                task_id = next_id("task")
                prep_tasks.append({
                    "task_id": task_id,
                    "plan_id": plan_id,
                    "user_id": user_id,
                    "scheduled_at": iso(scheduled),
                    "completed_at": iso(completed_at) if completed_at else "",
                    "task_type": task_type,
                    "topic_category": topic,
                    "status": "completed" if is_complete else rng.choice(["not_started", "in_progress"]),
                    "duration_minutes": rng.choice([25, 30, 40, 45, 60]),
                    "target_role": role,
                    "environment": "synthetic_demo",
                })
                if task_type in {"study", "revision", "coding"}:
                    add_event(user_id, scheduled, "note_opened", "study_notes", target_role=role, channel=channel, job_id=job_id, plan_id=plan_id)
                    add_generation(user_id, scheduled + timedelta(minutes=2), "study_notes", role)
                    if is_complete:
                        add_event(user_id, completed_at, "note_completed", "study_notes", target_role=role, channel=channel, job_id=job_id, plan_id=plan_id)
                        completed_study = True
                elif task_type == "exam" and is_complete:
                    exam_id = next_id("exam")
                    difficulty = rng.choices(DIFFICULTIES, weights=[0.18, 0.56, 0.26], k=1)[0]
                    base_score = min(88, max(38, rng.gauss(58 if difficulty == "Medium" else 64 if difficulty == "Easy" else 51, 11)))
                    attempts = 1 if rng.random() < 0.48 else 2 if rng.random() < 0.86 else 3
                    for attempt_no in range(1, attempts + 1):
                        attempt_start = completed_at + timedelta(days=(attempt_no - 1) * rng.randint(2, 6), minutes=rng.randint(1, 55))
                        if attempt_start > end_dt:
                            break
                        score = min(97, round(base_score + (attempt_no - 1) * rng.uniform(5.5, 13.5) + rng.gauss(0, 2.8), 1))
                        submit_at = attempt_start + timedelta(minutes=rng.choice([8, 10, 14, 19, 27]))
                        exam_attempts.append({
                            "attempt_id": next_id("attempt"),
                            "exam_id": exam_id,
                            "plan_id": plan_id,
                            "user_id": user_id,
                            "attempt_number": attempt_no,
                            "started_at": iso(attempt_start),
                            "submitted_at": iso(submit_at),
                            "score_pct": score,
                            "difficulty": difficulty,
                            "question_count": {"Easy": 10, "Medium": 20, "Hard": 40}[difficulty],
                            "target_role": role,
                            "acquisition_channel": channel,
                            "environment": "synthetic_demo",
                        })
                        add_event(user_id, attempt_start, "exam_started", "exams", target_role=role, channel=channel, job_id=job_id, plan_id=plan_id)
                        add_event(user_id, submit_at, "exam_submitted", "exams", target_role=role, channel=channel, job_id=job_id, plan_id=plan_id)
                        add_generation(user_id, attempt_start - timedelta(minutes=2), "exam_generation", role)
                        submitted_exam = True

            if completed_study:
                info["steps"]["First note completed"] = True
            if submitted_exam:
                info["steps"]["Exam submitted"] = True

            if submitted_exam and rng.random() < behavior["mock"]:
                mock_start = plan_at + timedelta(days=rng.randint(3, max(4, days_until)), hours=rng.randint(8, 20))
                if mock_start <= end_dt:
                    completed = rng.random() < 0.78
                    mock_end = mock_start + timedelta(minutes=rng.choice([18, 24, 31, 38])) if completed else None
                    scores = [row["score_pct"] for row in exam_attempts if row["plan_id"] == plan_id]
                    mock_score = min(96, round(mean(scores) + rng.uniform(-4, 8), 1)) if completed else ""
                    mock_interviews.append({
                        "mock_id": next_id("mock"),
                        "plan_id": plan_id,
                        "user_id": user_id,
                        "started_at": iso(mock_start),
                        "completed_at": iso(mock_end) if mock_end else "",
                        "status": "completed" if completed else "exited_early",
                        "average_score": mock_score,
                        "target_role": role,
                        "acquisition_channel": channel,
                        "environment": "synthetic_demo",
                    })
                    add_event(user_id, mock_start, "mock_interview_started", "mock_interviews", target_role=role, channel=channel, job_id=job_id, plan_id=plan_id)
                    add_generation(user_id, mock_start - timedelta(minutes=2), "mock_interview", role)
                    if completed:
                        add_event(user_id, mock_end, "mock_interview_completed", "mock_interviews", target_role=role, channel=channel, job_id=job_id, plan_id=plan_id)
                        info["steps"]["Mock interview completed"] = True

        # Subsequent sessions create realistic cohort behavior without inventing private content.
        if info["plans"]:
            weeks_available = max(0, min(12, ((END_DATE - signup.date()).days) // 7))
            for week in range(1, weeks_available + 1):
                return_probability = max(0.10, 0.64 * (0.84 ** (week - 1)))
                if rng.random() < return_probability:
                    session_at = signup + timedelta(days=week * 7 + rng.randint(0, 5), hours=rng.randint(7, 22))
                    if session_at <= end_dt:
                        add_event(user_id, session_at, "dashboard_opened", "dashboard", target_role=role, channel=channel, plan_id=rng.choice(info["plans"]))

    return {
        "users": users,
        "jobs": jobs,
        "prep_plans": prep_plans,
        "prep_tasks": prep_tasks,
        "exam_attempts": exam_attempts,
        "mock_interviews": mock_interviews,
        "ai_generations": ai_generations,
        "product_events": product_events,
        "state": state,
    }


def make_tableau_extracts(data: dict[str, list[dict]]) -> dict[str, list[dict]]:
    users = data["users"]
    events = data["product_events"]
    attempts = data["exam_attempts"]
    mocks = data["mock_interviews"]
    generations = data["ai_generations"]
    state = data["state"]

    daily = defaultdict(lambda: {"users": set(), "events": Counter()})
    for event in events:
        key = (event["occurred_at"][:10], event["acquisition_channel"], event["target_role"])
        daily[key]["users"].add(event["user_id"])
        daily[key]["events"][event["event_name"]] += 1
    daily_rows = []
    for (event_date, channel, role), value in sorted(daily.items()):
        counts = value["events"]
        daily_rows.append({
            "event_date": event_date,
            "acquisition_channel": channel,
            "target_role": role,
            "active_users": len(value["users"]),
            "signups": counts["account_created"],
            "job_saves": counts["job_saved"],
            "plans_generated": counts["prep_plan_generated"],
            "notes_completed": counts["note_completed"],
            "exams_submitted": counts["exam_submitted"],
            "mocks_completed": counts["mock_interview_completed"],
        })

    funnel_steps = ["Account created", "Logged in", "Job saved", "Prep plan generated", "First note completed", "Exam submitted", "Mock interview completed"]
    funnel = defaultdict(lambda: Counter())
    for user in users:
        info = state[user["user_id"]]
        key = (user["cohort_week"], user["acquisition_channel"], user["target_role"])
        for step in funnel_steps:
            if info["steps"].get(step):
                funnel[key][step] += 1
    funnel_rows = []
    for key, counts in sorted(funnel.items()):
        signup_count = counts["Account created"]
        previous = signup_count
        for order, step in enumerate(funnel_steps, start=1):
            reached = counts[step]
            funnel_rows.append({
                "cohort_week": key[0],
                "acquisition_channel": key[1],
                "target_role": key[2],
                "step_order": order,
                "funnel_step": step,
                "users_reached": reached,
                "conversion_from_signup": round(reached / signup_count, 4) if signup_count else 0,
                "conversion_from_previous_step": round(reached / previous, 4) if previous else 0,
            })
            previous = reached

    event_weeks = defaultdict(set)
    for event in events:
        event_weeks[event["user_id"]].add(monday(datetime.strptime(event["occurred_at"][:10], "%Y-%m-%d").date()))
    cohorts = defaultdict(list)
    for user in users:
        cohorts[user["cohort_week"]].append(user)
    retention_rows = []
    for cohort_week, cohort_users in sorted(cohorts.items()):
        cohort_start = datetime.strptime(cohort_week, "%Y-%m-%d").date()
        for weeks_since in range(0, 13):
            target_week = (cohort_start + timedelta(days=weeks_since * 7)).isoformat()
            retained = len([user for user in cohort_users if weeks_since == 0 or target_week in event_weeks[user["user_id"]]])
            retention_rows.append({
                "cohort_week": cohort_week,
                "weeks_since_signup": weeks_since,
                "cohort_size": len(cohort_users),
                "retained_users": retained,
                "retention_rate": round(retained / len(cohort_users), 4),
            })

    monthly_active = defaultdict(set)
    feature_usage = defaultdict(lambda: {"users": set(), "events": 0})
    for event in events:
        month = event["occurred_at"][:7]
        active_key = (month, event["target_role"])
        monthly_active[active_key].add(event["user_id"])
        key = (month, event["target_role"], event["feature"])
        feature_usage[key]["users"].add(event["user_id"])
        feature_usage[key]["events"] += 1
    feature_rows = []
    for (month, role, feature), value in sorted(feature_usage.items()):
        active = len(monthly_active[(month, role)])
        feature_rows.append({
            "event_month": month,
            "target_role": role,
            "feature": feature,
            "unique_users": len(value["users"]),
            "event_count": value["events"],
            "active_users": active,
            "adoption_rate": round(len(value["users"]) / active, 4) if active else 0,
        })

    user_attempts = defaultdict(list)
    for attempt in attempts:
        user_attempts[attempt["user_id"]].append(attempt)
    mock_by_user = defaultdict(list)
    for mock in mocks:
        mock_by_user[mock["user_id"]].append(mock)
    learning = defaultdict(lambda: {"first": [], "latest": [], "improvement": [], "learners": set(), "mock_started": 0, "mock_completed": 0, "mock_scores": []})
    for user_id, rows in user_attempts.items():
        ordered = sorted(rows, key=lambda row: row["submitted_at"])
        first, latest = ordered[0], ordered[-1]
        key = (latest["target_role"], latest["acquisition_channel"], latest["difficulty"])
        learning[key]["first"].append(float(first["score_pct"]))
        learning[key]["latest"].append(float(latest["score_pct"]))
        learning[key]["improvement"].append(float(latest["score_pct"]) - float(first["score_pct"]))
        if len(ordered) >= 2:
            learning[key]["learners"].add(user_id)
    for user_id, rows in mock_by_user.items():
        role = state[user_id]["role"]
        channel = state[user_id]["channel"]
        key = (role, channel, "All")
        learning[key]["mock_started"] += len(rows)
        completed = [row for row in rows if row["status"] == "completed"]
        learning[key]["mock_completed"] += len(completed)
        learning[key]["mock_scores"].extend(float(row["average_score"]) for row in completed)
    learning_rows = []
    for (role, channel, difficulty), value in sorted(learning.items()):
        learning_rows.append({
            "target_role": role,
            "acquisition_channel": channel,
            "exam_difficulty": difficulty,
            "learners_with_exam_attempts": len(value["first"]),
            "learners_with_multiple_attempts": len(value["learners"]),
            "average_first_exam_score": mean(value["first"]),
            "average_latest_exam_score": mean(value["latest"]),
            "average_score_improvement": mean(value["improvement"]),
            "mock_interviews_started": value["mock_started"],
            "mock_interviews_completed": value["mock_completed"],
            "mock_completion_rate": round(value["mock_completed"] / value["mock_started"], 4) if value["mock_started"] else 0,
            "average_mock_score": mean(value["mock_scores"]),
        })

    reliability = defaultdict(lambda: {"total": 0, "success": 0, "failure": 0, "latency": [], "tokens": 0})
    for event in generations:
        key = (event["occurred_at"][:10], event["feature"], event["target_role"])
        item = reliability[key]
        item["total"] += 1
        item[event["status"]] += 1
        item["latency"].append(int(event["latency_ms"]))
        item["tokens"] += int(event["total_tokens"])
    reliability_rows = []
    for (event_date, feature, role), value in sorted(reliability.items()):
        reliability_rows.append({
            "event_date": event_date,
            "feature": feature,
            "target_role": role,
            "total_generations": value["total"],
            "successful_generations": value["success"],
            "failed_generations": value["failure"],
            "success_rate": round(value["success"] / value["total"], 4),
            "average_latency_ms": mean(value["latency"]),
            "total_tokens": value["tokens"],
        })

    return {
        "tableau_daily_kpis": daily_rows,
        "tableau_activation_funnel": funnel_rows,
        "tableau_retention_cohorts": retention_rows,
        "tableau_feature_adoption": feature_rows,
        "tableau_learning_outcomes": learning_rows,
        "tableau_ai_reliability": reliability_rows,
    }


def load_sqlite(tables: dict[str, list[dict]]) -> None:
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        for name, rows in tables.items():
            if name == "state":
                continue
            columns = list(rows[0])
            connection.execute(f'DROP TABLE IF EXISTS "{name}"')
            definition = ", ".join(f'"{column}" TEXT' for column in columns)
            connection.execute(f'CREATE TABLE "{name}" ({definition})')
            placeholders = ", ".join("?" for _ in columns)
            connection.executemany(
                f'INSERT INTO "{name}" ({", ".join(chr(34) + column + chr(34) for column in columns)}) VALUES ({placeholders})',
                [[row[column] for column in columns] for row in rows],
            )
        connection.executescript(
            """
            CREATE INDEX idx_events_user_time ON product_events(user_id, occurred_at);
            CREATE INDEX idx_jobs_user ON jobs(user_id);
            CREATE INDEX idx_plans_user ON prep_plans(user_id);
            CREATE INDEX idx_attempts_user ON exam_attempts(user_id);
            CREATE VIEW vw_event_volume_by_day AS
            SELECT substr(occurred_at, 1, 10) AS event_date, event_name, feature, COUNT(*) AS events,
                   COUNT(DISTINCT user_id) AS unique_users
            FROM product_events
            GROUP BY 1, 2, 3;
            CREATE VIEW vw_exam_score_progression AS
            SELECT user_id, target_role, MIN(CAST(score_pct AS REAL)) AS minimum_score,
                   MAX(CAST(score_pct AS REAL)) AS maximum_score,
                   COUNT(*) AS attempts
            FROM exam_attempts
            GROUP BY 1, 2;
            """
        )
        connection.commit()
    finally:
        connection.close()


def main() -> None:
    if RAW_DIR.exists():
        shutil.rmtree(RAW_DIR)
    if TABLEAU_DIR.exists():
        shutil.rmtree(TABLEAU_DIR)
    RAW_DIR.mkdir(parents=True)
    TABLEAU_DIR.mkdir(parents=True)

    data = build_dataset()
    raw_tables = {name: rows for name, rows in data.items() if name != "state"}
    tableau_tables = make_tableau_extracts(data)
    for name, rows in raw_tables.items():
        write_csv(RAW_DIR / f"{name}.csv", rows)
    for name, rows in tableau_tables.items():
        write_csv(TABLEAU_DIR / f"{name}.csv", rows)
    load_sqlite(raw_tables)

    profile = {
        "dataset_label": "Synthetic demonstration data modeled from PrepInterview AI workflows. Not production usage.",
        "random_seed": SEED,
        "simulation_window": {"start": START_DATE.isoformat(), "end": END_DATE.isoformat()},
        "synthetic_users": USER_COUNT,
        "row_counts": {name: len(rows) for name, rows in raw_tables.items()},
        "tableau_extract_counts": {name: len(rows) for name, rows in tableau_tables.items()},
        "privacy": "Contains no real users, names, emails, job descriptions, answer text, prompts, or API secrets.",
    }
    PROFILE_PATH.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(profile, indent=2))


if __name__ == "__main__":
    main()
