# AllLife Bank — Credit Card Customer Segmentation

Unsupervised learning project that segments a bank's credit-card customer base to
support targeted marketing and a more efficient service-delivery model.

## Problem

AllLife Bank wants to grow its credit-card business through personalized campaigns
and to reduce the cost of poorly-rated support interactions. The goal was to find
distinct customer segments based on spending behavior and the channels customers use
to contact the bank, then translate those segments into concrete actions for the
marketing and operations teams.

## Data

660 customers, 5 behavioral features: average credit limit, total number of credit
cards, and contact counts across three channels (in-branch visits, online visits,
call-center calls). No missing values; a small number of duplicate customer keys were
reviewed during data checks.

## Approach

- Exploratory analysis and sanity checks on distributions and relationships
- Standardized the features and applied PCA to understand the dominant axes of variation
- Clustered with three methods — **K-Means**, **Gaussian Mixture Models**, and **K-Medoids** — to test whether the segment structure was stable across algorithms
- Selected the number of clusters using silhouette scores and business interpretability
- Profiled each segment and named it in plain business language

## Key Result

A **three-segment solution** that all three algorithms agreed on (K-Means and K-Medoids
produced identical assignments; silhouette ≈ 0.60):

| Segment | Size | Profile | Recommended action |
|---|---|---|---|
| Branch-Engaged Core Customers | ~58% | Moderate limits, multiple cards, highest branch use | Relationship-manager cross-sell, bundled products |
| Low-Value High-Support Callers | ~34% | Lowest limits, fewest cards, most calls | Self-service tools, call deflection, simpler products |
| Premium Digital Power Users | ~7% | Highest limits, most cards, heavy online use | Digital-first premium offers, concierge service, retention |

K-Means with three clusters is recommended for deployment because it gives strong
separation, clean business meaning, and is simple to operationalize in a CRM.

## Files

- `bank_customer_segmentation.ipynb` — full analysis with code, outputs, and plots

## Tools

Python · pandas · scikit-learn · scikit-learn-extra · matplotlib · seaborn

## Notes

Dataset is a standard public credit-card customer dataset used for segmentation
practice. Currency for the credit-limit field is unspecified in the source data.
