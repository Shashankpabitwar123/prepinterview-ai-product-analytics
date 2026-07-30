# Dashboard findings

> **Synthetic-data reminder:** Every figure below comes from deterministic
> demonstration data modeled on PrepInterview AI workflows. These are
> portfolio-analysis findings, not production-user or business results.

## Activation funnel

| Step | Synthetic users reached | Share of signups |
| --- | ---: | ---: |
| Account created | 8,000 | 100.0% |
| Logged in | 7,274 | 90.9% |
| Job saved | 4,858 | 60.7% |
| Prep plan generated | 3,498 | 43.7% |
| First note completed | 3,492 | 43.6% |
| Exam submitted | 2,526 | 31.6% |
| Mock interview completed | 958 | 12.0% |

The first large synthetic funnel drop occurs between login and job saving.
Mock-interview completion is the smallest downstream action. The dashboard
should frame these as areas for future investigation, not as evidence that a
product change caused a specific outcome.

## Learning outcomes

Across users with more than one synthetic exam attempt, every modeled role
shows a higher latest score than first score. The modeled average gain ranges
from 5.6 to 7.8 percentage points:

| Target role | Learners | First score | Latest score | Gain |
| --- | ---: | ---: | ---: | ---: |
| Software Engineer | 521 | 57.4% | 65.2% | +7.8 pts |
| Product Manager | 480 | 57.2% | 63.4% | +6.2 pts |
| UX Designer | 526 | 58.1% | 64.1% | +6.0 pts |
| Finance Analyst | 514 | 58.1% | 63.6% | +5.6 pts |
| Data Analyst | 485 | 58.2% | 63.8% | +5.6 pts |

This is a practice-progression signal in a simulated dataset. It does not show
that PrepInterview AI improves actual interview outcomes.

## AI reliability

The modeled AI workflow has a 93.85% to 95.48% success-rate range across
features. Study-note generation has the highest average latency (2,148 ms),
while mock-interview generation has the lowest modeled success rate (93.85%).
The Tableau dashboard should pair reliability and latency; lower latency by
itself is not a quality outcome.

## Retention cohorts

Average synthetic cohort retention is 44.3% at week 1, 24.5% at week 4, 6.5%
at week 8, and 2.4% at week 12. Cohorts near the end of the six-month
simulation have shorter observation windows, so the dashboard must make the
date range visible and avoid direct cohort comparisons without equal exposure.
