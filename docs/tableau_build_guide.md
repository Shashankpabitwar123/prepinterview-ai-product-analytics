# Tableau build guide

> Add the synthetic-data disclosure from `TABLEAU_PUBLIC_DISCLOSURE.txt` to the footer of every dashboard before publishing.

## Connect these Tableau-ready files

Connect each CSV separately from `data/tableau/`:

1. `tableau_daily_kpis.csv`
2. `tableau_activation_funnel.csv`
3. `tableau_retention_cohorts.csv`
4. `tableau_feature_adoption.csv`
5. `tableau_learning_outcomes.csv`
6. `tableau_ai_reliability.csv`

Do not use the raw entity-level CSVs in Tableau Public. They are included only for auditability and SQL validation.

## Dashboard 1 — Product Overview

Use `tableau_daily_kpis.csv`.

- KPI cards: signups, active users, plans generated, exams submitted, mock interviews completed
- Line chart: weekly active users
- Dual-axis trend: plans generated and exam submissions
- Stacked bar: target role by active users
- Filters: date, acquisition channel, target role

Story question: **Is the synthetic product journey producing meaningful preparation activity after signup?**

## Dashboard 2 — Activation Funnel

Use `tableau_activation_funnel.csv`.

- Funnel: `funnel_step` ordered by `step_order`, sized by `users_reached`
- Label: `conversion_from_signup`
- Heatmap: cohort week by funnel step
- Segmented bar: conversion by acquisition channel
- Filters: cohort week, channel, role

Story question: **Where does the journey lose potential learners: login, job capture, plan generation, study, assessment, or mock practice?**

## Dashboard 3 — Retention and Feature Adoption

Use `tableau_retention_cohorts.csv` and `tableau_feature_adoption.csv` as separate worksheets on the same dashboard.

- Cohort heatmap: `cohort_week` by `weeks_since_signup`, color `retention_rate`
- Area/line chart: feature adoption by month
- Bar chart: feature adoption by target role
- Filters: role and month

Story question: **Which PrepInterview AI features create repeat preparation behavior?**

## Dashboard 4 — Learning Outcomes and AI Reliability

Use `tableau_learning_outcomes.csv` and `tableau_ai_reliability.csv`.

- Dumbbell chart: average first versus latest exam score by role
- Bar chart: average score improvement by difficulty
- KPI cards: mock completion rate, average mock score, AI success rate, average latency
- Line chart: AI success rate over time
- Detail table: generation feature, total generations, latency, and total tokens

Story question: **Do engaged learners show practice-score improvement while the AI workflow remains reliable?**

## Visual standard

- Use a restrained dark navy/blue product-analytics theme with one accent color for successful progression and orange/red only for failures/drop-off.
- Avoid pie charts for funnel or retention comparisons.
- Keep the dashboard title explicit: `PrepInterview AI Product Analytics Prototype — Synthetic Demo Data`.
- In the subtitle, say the product workflow is real and the dataset is synthetic.
- Never remove the footer disclosure.
