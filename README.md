# PrepInterview AI Product Analytics Prototype — Tableau

> **Synthetic demonstration data modeled from PrepInterview AI workflows. This package does not represent production users, customer traction, or business performance.**

This is a portfolio analytics package for the real PrepInterview AI product. It models the product journey from account creation through job capture, AI planning, notes, exams, mock interviews, and returning engagement. The product workflow is real; the analytics records are deterministic synthetic data because the live product does not yet have an adequate user base for population-level analysis.

## What this package demonstrates

- Product event taxonomy and privacy-safe instrumentation design
- Relational product-event modeling across users, jobs, plans, tasks, exams, mock interviews, and AI generation
- Funnel, cohort-retention, feature-adoption, learning-outcome, and AI-reliability analysis
- Reproducible synthetic data generation and data-quality checks
- Tableau-ready aggregate extracts, SQL evidence, and dashboard build instructions

## Important integrity boundary

Use this on a résumé or GitHub as a **product analytics prototype**. Do not describe the figures as actual PrepInterview AI user behavior or claim that the work improved retention, activation, revenue, or customer outcomes.

Recommended résumé wording:

> Designed a Tableau product-analytics prototype for PrepInterview AI using a documented synthetic event model, analyzing activation funnels, feature adoption, retention cohorts, AI reliability, and interview-score progression.

## Folder guide

- `data/raw_synthetic/` — locally generated linked entity-level synthetic tables and event records; excluded from Git to keep the public repository compact
- `data/tableau/` — public-safe aggregate CSVs to connect in Tableau Public
- `data/prepinterview_synthetic_analytics.db` — locally generated SQLite analysis database with source tables and views; excluded from Git
- `data/data_profile.json` — dataset lineage and row counts
- `docs/` — metric definitions, event taxonomy, data-quality report, findings, public disclosure, and Tableau build guide
- `sql/` — inspectable analytical SQL
- `scripts/` — reproducible generator and validator

## Rebuild the package

```bash
python3 scripts/generate_synthetic_data.py
python3 scripts/validate_dataset.py
```

The generator uses a fixed seed, so each rebuild produces the same dataset and results.

## Tableau entry point

**Live Tableau Story:** [PrepInterview AI — Synthetic Product Analytics](https://public.tableau.com/app/profile/shashank.pabitwar/viz/PrepInterview_AI_Product_Analytics_Final/StoryPrepInterviewAIProductAnalytics?publish=yes)

The public Story contains four navigable dashboards:

1. Product Overview
2. Activation Funnel
3. Retention & Feature Adoption
4. Learning Outcomes & AI Reliability

The packaged, reproducible workbook is [tableau/PrepInterview_AI_Product_Analytics_Final.twbx](tableau/PrepInterview_AI_Product_Analytics_Final.twbx). It embeds the six public-safe aggregate extracts from `data/tableau/`.

Every published dashboard includes the required synthetic-data disclosure from `docs/TABLEAU_PUBLIC_DISCLOSURE.txt`.

Before publishing, use the [dashboard QA checklist](docs/dashboard_qa_checklist.md). The [dashboard findings](docs/dashboard_findings.md) and [portfolio summary](docs/portfolio_summary.md) provide the source-backed narrative and résumé-ready wording.
