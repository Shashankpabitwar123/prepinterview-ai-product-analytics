-- PrepInterview AI Product Analytics Prototype
-- Synthetic demo data only. These queries are designed for SQLite.

-- 1. Daily product activity
SELECT
  substr(occurred_at, 1, 10) AS event_date,
  target_role,
  acquisition_channel,
  COUNT(DISTINCT user_id) AS active_users,
  SUM(event_name = 'prep_plan_generated') AS plans_generated,
  SUM(event_name = 'exam_submitted') AS exams_submitted,
  SUM(event_name = 'mock_interview_completed') AS mock_interviews_completed
FROM product_events
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3;

-- 2. Event-level funnel counts
SELECT
  event_name,
  COUNT(DISTINCT user_id) AS users_reached
FROM product_events
WHERE event_name IN (
  'account_created', 'login_completed', 'job_saved', 'prep_plan_generated',
  'note_completed', 'exam_submitted', 'mock_interview_completed'
)
GROUP BY 1
ORDER BY CASE event_name
  WHEN 'account_created' THEN 1 WHEN 'login_completed' THEN 2
  WHEN 'job_saved' THEN 3 WHEN 'prep_plan_generated' THEN 4
  WHEN 'note_completed' THEN 5 WHEN 'exam_submitted' THEN 6
  WHEN 'mock_interview_completed' THEN 7 END;

-- 3. Exam-score improvement by role
WITH ordered_attempts AS (
  SELECT
    user_id,
    target_role,
    CAST(score_pct AS REAL) AS score_pct,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY submitted_at) AS first_rank,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY submitted_at DESC) AS latest_rank
  FROM exam_attempts
), per_user AS (
  SELECT
    user_id,
    target_role,
    MAX(CASE WHEN first_rank = 1 THEN score_pct END) AS first_score,
    MAX(CASE WHEN latest_rank = 1 THEN score_pct END) AS latest_score
  FROM ordered_attempts
  GROUP BY 1, 2
)
SELECT
  target_role,
  COUNT(*) AS learners,
  ROUND(AVG(first_score), 2) AS average_first_score,
  ROUND(AVG(latest_score), 2) AS average_latest_score,
  ROUND(AVG(latest_score - first_score), 2) AS average_score_improvement
FROM per_user
GROUP BY 1
ORDER BY average_score_improvement DESC;
