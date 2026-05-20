# Ebola Outbreak Analytics — Portfolio Project

**Author:** Jermaine
**Stack:** Python, pandas, matplotlib, scikit-learn

---

## Executive summary (read this first)

For reviewers who want the findings without reading code, start here:

[**Executive Summary (PDF)**](./ebola_analytics_portfolio_report.pdf)

This one-document writeup answers all eight portfolio questions in plain English, with the key tables and charts, and finishes with a code appendix.

---

## What this project is

An end-to-end exploratory data analysis of historical Ebola outbreaks, structured around eight analyst-style business questions:

1. Which countries were most affected by Ebola, and why?
2. What factors are most associated with high fatality rates?
3. How have Ebola outbreaks changed over time?
4. Which virus species is most dangerous?
5. Can Ebola deaths be predicted from outbreak characteristics?
6. What transmission factors most influence outbreak spread?
7. Are hospitalization and survival related?
8. What trends emerge before large outbreaks?

The dataset is small and is intended for portfolio practice rather than public-health decision-making. The notebook is transparent about this throughout.

---

## Repository contents

| File | Purpose |
|------|---------|
| [`ebola_analytics_portfolio_report.pdf`](./ebola_analytics_portfolio_report.pdf) | Polished executive summary — recommended starting point for non-technical reviewers. |
| [`Ebola_Portfolio_Analysis.ipynb`](./Ebola_Portfolio_Analysis.ipynb) | Full reproducible analysis in Jupyter, with code, charts, and written conclusions for each question. |
| `ebola_extracted/` | Source CSVs used by the notebook (place alongside the notebook before running). |

---

## How to run the notebook

```bash
# 1. Create and activate a fresh environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate            # macOS / Linux
# .venv\Scripts\activate             # Windows

# 2. Install dependencies
pip install pandas numpy matplotlib scikit-learn jupyter

# 3. Launch
jupyter notebook Ebola_Portfolio_Analysis.ipynb
```

The notebook expects the source CSVs in a folder named `ebola_extracted/` next to it. Adjust the `DATA_DIR` variable in the first code cell if your files live elsewhere.

---

## Methodology highlights

- **EDA:** Cleaned dates, derived a categorical risk score, and built per-question tables grouped by country, year, species, and transmission factor.
- **Visualization:** Bar charts, time series, and scatter plots in matplotlib for each of the eight questions.
- **Predictive modeling (Question 5):** Predicts outbreak deaths from `cases` and `fatality_rate` using **Ridge regression** with **Leave-One-Out Cross-Validation (LOOCV)**. Because the outbreak table has only a handful of rows, LOOCV provides an honest out-of-sample R² / MAE rather than the inflated metrics you would get from fitting and scoring on the same data.
- **Honest caveats:** Sample sizes for several virus species and clinical outcomes are very small. Findings are presented as exploratory.

---

## Key findings (one-line each)

- Sierra Leone, Liberia, Guinea, and the DRC absorbed the largest share of cases and deaths.
- The strongest evidence-backed transmission drivers are direct contact with body fluids, insufficient PPE, and unsafe caregiving practices.
- The 2014–2016 West Africa epidemic dominates the time series in both cases and deaths.
- *Ebola virus* (the species) accounts for the vast majority of human impact in this dataset.
- Deaths can be modeled from outbreak size and fatality rate, but the dataset is too small for real-world forecasting — the model is a demonstration of cross-validated regression on small data.

For full numbers, charts, and reasoning, see [the executive summary](./ebola_analytics_portfolio_report.pdf) or open the notebook.

---

## Limitations

- Small sample size across every sub-table (countries, species, clinical patients, monthly trends).
- All clinical records are hospitalized patients, so hospitalization vs. non-hospitalization cannot be compared directly.
- Monthly data does not include enough pre-outbreak observations to validate early-warning signals.

---

## License

This is a personal portfolio project. The dataset is illustrative and not intended for clinical or operational use.
