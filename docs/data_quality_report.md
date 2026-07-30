# Data quality report

> **Dataset disclosure:** This is a synthetic demonstration dataset modeled from PrepInterview AI workflows. It is not production usage data.

**Result:** 24/24 checks passed.

| Check | Result | Evidence |
| --- | --- | --- |
| Required raw tables exist | PASS | Found: ai_generations, exam_attempts, jobs, mock_interviews, prep_plans, prep_tasks, product_events, users |
| users primary key uniqueness | PASS | 8,000 unique IDs across 8,000 rows |
| jobs primary key uniqueness | PASS | 6,929 unique IDs across 6,929 rows |
| prep_plans primary key uniqueness | PASS | 4,491 unique IDs across 4,491 rows |
| prep_tasks primary key uniqueness | PASS | 51,788 unique IDs across 51,788 rows |
| exam_attempts primary key uniqueness | PASS | 7,485 unique IDs across 7,485 rows |
| mock_interviews primary key uniqueness | PASS | 1,285 unique IDs across 1,285 rows |
| ai_generations primary key uniqueness | PASS | 57,195 unique IDs across 57,195 rows |
| product_events primary key uniqueness | PASS | 125,044 unique IDs across 125,044 rows |
| Job-to-user referential integrity | PASS | 0 orphan jobs |
| Plan-to-job/user referential integrity | PASS | 0 orphan plans |
| Task-to-plan/user referential integrity | PASS | 0 orphan tasks |
| Exam-attempt referential integrity | PASS | 0 orphan attempts |
| Mock-interview referential integrity | PASS | 0 orphan mocks |
| Exam score range | PASS | 0 out-of-range scores |
| Completed mock scores present | PASS | 0 completed mocks missing scores |
| Synthetic environment marker | PASS | 0 events without synthetic_demo marker |
| No prohibited public-data columns | PASS | Present prohibited columns: none |
| Funnel is non-increasing by segment | PASS | 0 invalid funnel segments |
| Retention rate bounds | PASS | 0 invalid retention rows |
| Retention cohort week 0 baseline | PASS | 0 invalid week-0 rows |
| AI reliability totals reconcile | PASS | 0 non-reconciling rows |
| SQLite user count matches CSV | PASS | SQLite=8,000; CSV=8,000 |
| SQLite event view reconciles | PASS | View=125,044; source=125,044 |

## Dashboard readiness

The Tableau extracts are safe for a public synthetic-demo dashboard: they contain aggregate metrics and do not include names, emails, job descriptions, answer text, prompts, or source URLs.

## Required Tableau disclosure

Place this sentence in every published dashboard footer: `Synthetic demonstration data modeled from PrepInterview AI workflows; it does not represent production users or business performance.`
