# 4th-Grade Math Interim Assessment Analysis

Turning real classroom assessment data into instructional decisions: where to spend
re-teaching time, and which students need which kind of support.

## Why this project

Most analytics portfolios use the same public practice datasets. This one uses real data
from my own 4th-grade math classroom (two interim assessments, 2025–2026 school year) and
answers the question a teacher or instructional coach actually has to answer: *given these
results, what do we do Monday morning?*

**Student privacy:** all names and ID numbers are stripped and replaced with anonymous
labels (S01, S02, …) by `prepare_data.py` before any analysis runs. The raw files and the
real-name mapping are **never** committed to this repository (see `.gitignore`). Nothing in
the published notebook can identify a student.

## The analysis

The notebook ([`grade4_math_analysis.ipynb`](./grade4_math_analysis.ipynb)) walks through:

1. **Class overview** — score distributions on each interim
2. **Growth** — matched per-student change from Interim 1 to Interim 2
3. **Standards / skill gaps** — class mastery on each Tennessee math standard
4. **Item analysis** — the specific questions that revealed shared misconceptions
5. **Tiered grouping** — students sorted into four instructional groups with actions

## Key findings

- The class splits into four instructional tiers: **9** ready for enrichment, **11**
  on-track, **12** needing targeted support, and **9** needing intensive support.
- The class average dipped ~5 points between the two interims — but this was **not broad
  regression.** Interim 2 added the year's hardest standards (multi-step word problems and
  division). The dip is concentrated in that new, higher-rigor content, which is a very
  different instructional conclusion than "students forgot what they learned."
- **Weakest skills:** multi-step word problems (~46% mastery) and multi-digit
  multiplication (~57%). **Strongest:** add/subtract (~89%) and comparing multi-digit
  numbers (~90%).
- One item — a multi-step word problem — was answered correctly by only **17%** of the
  class, flagging a shared misconception worth a whole-class mini-lesson.

![Standards mastery](outputs/standards_mastery.png)

![Instructional tiers](outputs/instructional_tiers.png)

## Recommendations (in the notebook)

A short whole-class unit on word-problem strategy, a targeted small group for
multiplication fluency and rounding, scaffolded intensive support for the lowest tier
cross-referenced against the largest individual score drops, and enrichment problems for
the top tier.

## How to run

```bash
# place the raw exports in raw/ (not committed), then:
python prepare_data.py        # anonymizes -> data/ and private/
jupyter notebook grade4_math_analysis.ipynb   # Restart & Run All
```

## Project structure

```
grade4-math-analysis/
├── README.md
├── prepare_data.py              # anonymization + feature building
├── grade4_math_analysis.ipynb   # the analysis (plots render inline)
├── data/                        # anonymized, safe to share
│   ├── interim1_anon.csv
│   ├── interim2_anon.csv
│   ├── standards_long.csv
│   ├── student_growth.csv
│   └── item_analysis.csv
├── outputs/                     # exported charts for this README
└── private/                     # NEVER committed (see .gitignore)
    └── student_id_map.csv
```

## Tools

Python · pandas · NumPy · matplotlib

## Limitations

The two interims are different tests, so growth is read in context rather than as a clean
pre/post. This is a single class (n≈41), so findings guide this classroom's instruction and
are not generalizable. Per-standard "mastery" is percent-correct over a small number of
items (3–6 each), so any one standard's figure is sensitive to one or two questions.
