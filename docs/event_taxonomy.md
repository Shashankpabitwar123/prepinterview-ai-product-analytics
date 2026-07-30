# Product event taxonomy

The data model follows the real PrepInterview AI workflow: capture a job, generate a plan, study, take an exam, run a mock interview, and return to prepare further.

| Event | Feature | Trigger | Required safe properties | Never include |
| --- | --- | --- | --- | --- |
| `account_created` | `auth` | Account successfully created | acquisition channel, role category | email, password, OTP |
| `login_completed` | `auth` | Authenticated session established | session ID, client platform | token or IP address |
| `job_saved` | `jobs` | Job description/URL saved | source type, role category | job description, URL, company name if public release |
| `job_analysis_completed` | `jobs` | AI job analysis returns | role category, generation status | generated analysis content |
| `prep_plan_generated` | `prep_plans` | Plan persisted | days until interview, task count | full plan text |
| `note_opened` | `study_notes` | User opens a study note | topic category | note body, question, answer |
| `note_completed` | `study_notes` | Study task marked complete | topic category, duration bucket | note body |
| `exam_started` | `exams` | Timed exam begins | difficulty, question-count bucket | questions or answers |
| `exam_submitted` | `exams` | Exam submitted | difficulty, score, completion status | answer text, feedback text |
| `mock_interview_started` | `mock_interviews` | Mock session begins | role category, interview format | transcript/audio |
| `mock_interview_completed` | `mock_interviews` | Mock session completed | score, completion status | transcript/audio |
| `dashboard_opened` | `dashboard` | Returning authenticated session | plan presence | page content |

## Future production instrumentation

Keep `UserUsageEvent` for AI usage and token-cost auditing. Add a separate `ProductEvent` model for product funnel telemetry so AI-cost records and user-behavior records retain clear, stable meanings.

Recommended fields:

```text
event_id, user_id, anonymous_session_id, occurred_at, event_name, feature,
job_id, prep_plan_id, role_category, source_type, client_platform,
app_version, properties_json
```

For production, retain raw events privately in Neon/PostgreSQL. Export only aggregate, privacy-reviewed tables for Tableau Public.
