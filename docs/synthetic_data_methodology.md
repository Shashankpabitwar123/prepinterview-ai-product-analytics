# Synthetic data methodology

## Purpose

The live PrepInterview AI product has no sufficient user base for an honest population-level product analysis. This dataset exists to demonstrate a real analytics design using the product's actual workflow and data relationships.

## Simulation boundary

- Window: January 1, 2026 through June 30, 2026
- Population: 8,000 synthetic user records
- Reproducibility: deterministic random seed `20260728`
- Unit of analysis: synthetic users, jobs, plans, tasks, attempts, sessions, and product events
- Prohibited data: no real user accounts, emails, job descriptions, answer text, prompts, transcripts, source URLs, or secrets

## Behavior rules

The generator creates linked records rather than disconnected random tables:

1. A synthetic user signs up through a modeled acquisition channel.
2. Some users log in; a subset saves one or more jobs.
3. A subset of saved jobs receives a prep plan.
4. Plans create realistic scheduled tasks across notes, exams, coding, mock interviews, and revision.
5. Users may abandon, partially complete, or complete journeys.
6. Exam scores may improve across repeat attempts, with bounded gains and normal variation.
7. Mock interviews require prior exam engagement, preserving a valid funnel sequence.
8. Returning sessions decay over subsequent weeks to create cohort patterns.

## Why the values are intentionally not treated as findings

The conversion rates, score changes, and channel differences exist only to exercise calculations, filters, cohorts, and dashboard storytelling. They are not market research, user research, or evidence of product performance.

## Public-dashboard disclosure

Copy the exact disclosure from `TABLEAU_PUBLIC_DISCLOSURE.txt` into the footer of every published dashboard.
