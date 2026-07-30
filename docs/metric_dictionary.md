# Metric dictionary

> **Scope:** synthetic product-analytics prototype. Definitions are implementation-ready but the values are not real customer metrics.

## Primary KPIs

| Metric | Definition | Formula | Decision supported | Guardrail |
| --- | --- | --- | --- | --- |
| Activation rate | New users who generate a prep plan and complete at least one study note within the selected window | `users reaching First note completed / account-created users` | Whether onboarding creates an initial learning action | Do not compare channels without equal observation windows |
| Preparation engagement | Scheduled preparation tasks completed across active plans | `completed prep tasks / scheduled prep tasks` | Whether plans are practical and actionable | Separate task types; an exam is not equivalent to a note |
| Learning improvement | Score gain from a user's first to latest submitted exam attempt | `latest exam score - first exam score` | Whether practice is associated with stronger performance | This is not causal evidence of interview success |

## Funnel metrics

| Funnel step | Event or entity rule | Denominator |
| --- | --- | --- |
| Account created | `account_created` | None — starting cohort |
| Logged in | `login_completed` | Account-created users |
| Job saved | `job_saved` | Account-created users |
| Prep plan generated | `prep_plan_generated` | Account-created users |
| First note completed | `note_completed` at least once | Account-created users |
| Exam submitted | `exam_submitted` at least once | Account-created users |
| Mock interview completed | `mock_interview_completed` at least once | Account-created users |

## Supporting metrics

| Metric | Definition | Notes |
| --- | --- | --- |
| Weekly retention | Users with a non-signup product event in a week after their signup week | Week 0 is the full signup cohort by definition |
| Feature adoption | Unique active users who used a feature in a month | `feature users / monthly active users` |
| Mock completion rate | Completed mock sessions divided by started mock sessions | Early exits are intentionally counted as incomplete |
| AI success rate | Successful AI generations divided by all AI generations | Analyze by feature, role, and date |
| Average AI latency | Average generation latency in milliseconds | Pair with success rate; lower latency alone is not success |

## Interpretation limits

- Score improvement is a practice signal, not proof of eventual interview outcomes.
- Retention is behavioral recurrence, not paid retention or revenue retention.
- Acquisition-channel comparisons are simulated and must not be interpreted as marketing performance.
- The dashboard must show the synthetic-data disclosure in its footer.
