# PrepInterview AI — Product Analytics Case Study

> A Tableau and SQL portfolio case study built around the real PrepInterview AI workflow, using documented **synthetic demonstration data**. It does not represent real customers, product traction, or business performance.

## Start here

| Resource | Link |
| --- | --- |
| Live PrepInterview AI product | [prepinterviewai.com](https://prepinterviewai.com) |
| Product source code | [InterviewPrep AI GitHub repository](https://github.com/Shashankpabitwar123/interviewPrep_AI) |
| Interactive analytics Story | [Open the four-page Tableau Story](https://public.tableau.com/app/profile/shashank.pabitwar/viz/PrepInterview_AI_Product_Analytics_Final/StoryPrepInterviewAIProductAnalytics?publish=yes) |
| Downloadable analytics workbook | [Final Tableau packaged workbook](tableau/PrepInterview_AI_Product_Analytics_Final.twbx) |

For the fastest review, open the Tableau Story and use its four-page navigator.

## 1. The product behind the analysis

[PrepInterview AI](https://prepinterviewai.com) is an AI interview-preparation platform. A user can capture or paste a job description, save a job, generate a day-by-day prep plan, study AI-generated notes, take role-specific exams, practice mock interviews, and track preparation progress.

The live application is a separate software product. This repository is its analytics companion case study. It models the product workflow so the analysis can demonstrate product-analytics skills without presenting simulated records as real user telemetry.

## 2. What questions does the analysis answer?

- Where do modeled users drop off between signup, job saving, plan generation, learning, and mock interviews?
- How does modeled feature adoption change by month and target role?
- What does modeled cohort retention look like over the first 12 weeks?
- How do modeled exam scores progress across target roles and difficulty levels?
- How do modeled AI-generation success rate and latency vary by feature?

## 3. Tableau Story: four dashboards

| Page | Dashboard | What to look for |
| ---: | --- | --- |
| 1 | Product Overview | Core activity KPIs, weekly preparation activity, role-level plan generation, and acquisition-channel mix. |
| 2 | Activation Funnel | Modeled progression from account creation through completed mock interviews, filterable by role and acquisition channel. |
| 3 | Retention & Feature Adoption | Weekly cohort-retention heatmap, feature-adoption trend, and adoption comparison by role. |
| 4 | Learning Outcomes & AI Reliability | Modeled score improvement by role plus AI success-rate and latency comparisons by feature. |

## 4. Example findings — synthetic data only

- The modeled activation funnel goes from 8,000 accounts created to 958 mock interviews completed (12.0% of synthetic signups).
- In the simulated exam data, modeled first-to-latest score gains range from 5.6 to 7.8 percentage points by role.
- Modeled AI success rates range from 93.85% to 95.48%; study-note generation has the highest modeled average latency.
- Average modeled cohort retention is 44.3% at week 1 and 24.5% at week 4.

Read the full, source-backed interpretation in [dashboard findings](docs/dashboard_findings.md). These observations identify questions to investigate if real telemetry is collected; they are not claims of product impact, causality, or customer outcomes.

## 5. Skills demonstrated

- Tableau dashboard design, interactive Story navigation, and Tableau Public publishing
- Product funnel, cohort-retention, feature-adoption, learning-outcome, and AI-reliability analysis
- SQL analysis and reproducible synthetic-event modeling
- Metric definitions, event taxonomy, data quality, and privacy-safe public extracts
- Clear stakeholder storytelling with documented limitations

## 6. Repository guide

| Folder | Contents |
| --- | --- |
| [`tableau/`](tableau/) | Final packaged workbook and live Story link. |
| [`data/tableau/`](data/tableau/) | Six compact, public-safe CSV extracts used by Tableau. |
| [`sql/`](sql/) | Inspectable analysis queries. |
| [`scripts/`](scripts/) | Deterministic generator, validator, and GitHub publishing helper. |
| [`docs/`](docs/) | Methodology, event taxonomy, metric dictionary, QA checklist, findings, and disclosure text. |
| [`data/data_profile.json`](data/data_profile.json) | Simulation period, row counts, extract counts, and privacy boundary. |

The raw synthetic entity tables and local SQLite database are intentionally excluded from GitHub. They can be recreated with the included scripts.

## 7. Reproduce and validate

```bash
python3 scripts/generate_synthetic_data.py
python3 scripts/validate_dataset.py
```

The generator uses a fixed seed, so a rebuild produces the same demonstration dataset. The validation suite checks key uniqueness, referential integrity, score ranges, funnel logic, retention bounds, AI-reliability reconciliation, and public-data safety.

## 8. Data and ethics boundary

This analysis is based on deterministic synthetic records generated from the real PrepInterview AI workflow. It contains no real users, names, email addresses, job descriptions, prompts, answer text, or API secrets.

Use this project on a résumé as a **product analytics prototype**. Do not claim that the dashboard measures actual PrepInterview AI user behavior, retention, revenue, experimentation results, or business impact. See the full [synthetic-data methodology](docs/synthetic_data_methodology.md) and [public disclosure](docs/TABLEAU_PUBLIC_DISCLOSURE.txt).
