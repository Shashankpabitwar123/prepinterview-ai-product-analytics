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

- `data/raw_synthetic/` — linked entity-level synthetic tables and event records
- `data/tableau/` — public-safe aggregate CSVs to connect in Tableau Public
- `data/prepinterview_synthetic_analytics.db` — SQLite analysis database with source tables and views
- `data/data_profile.json` — dataset lineage and row counts
- `docs/` — metric definitions, event taxonomy, data-quality report, public disclosure, and Tableau build guide
- `sql/` — inspectable analytical SQL
- `scripts/` — reproducible generator and validator

## Rebuild the package

```bash
python3 scripts/generate_synthetic_data.py
python3 scripts/validate_dataset.py
```

The generator uses a fixed seed, so each rebuild produces the same dataset and results.

## Tableau entry point

Open Tableau Public and connect to the six CSVs in `data/tableau/`. Follow [the Tableau build guide](docs/tableau_build_guide.md). Every published dashboard must include the required synthetic-data disclosure from `docs/TABLEAU_PUBLIC_DISCLOSURE.txt`.
