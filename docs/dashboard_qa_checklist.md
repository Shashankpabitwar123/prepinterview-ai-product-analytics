# Tableau dashboard QA checklist

Use this after the workbook is built and before it is published.

## Scope and disclosure

- [ ] Dashboard title says `PrepInterview AI Product Analytics Prototype — Synthetic Demo Data`.
- [ ] The subtitle says the product workflow is real and the dataset is synthetic.
- [ ] Every dashboard includes the disclosure from `TABLEAU_PUBLIC_DISCLOSURE.txt`.
- [ ] No chart or caption implies real customers, traction, revenue, causality, or experimentation.

## Metric validation

- [ ] Product Overview totals reconcile to `data/data_profile.json`.
- [ ] The funnel starts at 8,000 synthetic signups and each later step is non-increasing.
- [ ] Retention week 0 is 100% for each cohort.
- [ ] Feature-adoption rate stays between 0% and 100%.
- [ ] Latest exam score and score-gain views use the documented first-versus-latest logic.
- [ ] AI success rate equals successful generations divided by all generations.

## Interaction and presentation

- [ ] Date, target-role, and acquisition-channel filters update only the views they support.
- [ ] Filters have explicit labels and no empty/ambiguous default state.
- [ ] Tooltip labels state the denominator for rates.
- [ ] Dashboard text remains readable at normal Tableau Public viewing size.
- [ ] Dark-navy/blue surfaces and accent colors preserve adequate contrast.
- [ ] Funnel and retention comparisons use bars/heatmaps, not pie charts.

## Publish evidence

- [ ] Save the packaged workbook as `tableau/PrepInterview_AI_Product_Analytics_Prototype.twbx`.
- [ ] Publish the workbook to Tableau Public.
- [ ] Record the public URL in `README.md`.
- [ ] Export one PDF and capture one screenshot per dashboard in `docs/evidence/`.
- [ ] Verify the published view in an incognito/private browser window.
