# Vintage Vehicle Segmentation with PCA & t-SNE

Dimensionality-reduction and clustering project that groups vintage vehicles into
market segments to support differentiated merchandising for a used-car dealership.

## Problem

SecondLife, a used-car dealership shifting its focus to vintage cars, wants to use its
historical sales data to find natural groupings of vehicles so it can target different
buyer audiences more efficiently. The goal was to reduce a set of correlated vehicle
attributes down to their underlying structure and identify clear, marketable segments.

## Data

The Auto MPG dataset — 398 vehicles with attributes including miles per gallon,
cylinders, displacement, horsepower, weight, acceleration, model year, and car name.

## Approach

- Cleaned the `horsepower` field (stored as text with `?` for missing values) and
  imputed missing entries with the median
- Engineered interpretive features: full model year, brand (from the car name), and a
  model-year era bucket
- Standardized the numeric features
- Applied **PCA** to interpret the dominant axes of variation and visualize the data
  in two dimensions
- Applied **t-SNE** as a non-linear check on the cluster structure
- Used **K-Means** to assign segments, then profiled them across the original variables

## Key Result

A **two-segment** structure:

- **Efficiency-oriented segment** — lighter, more fuel-efficient, lower-powered
  vehicles; the larger group, concentrated in later model years and in brands like
  Toyota, Datsun, and Volkswagen. Position as practical, accessible classics.
- **Performance / collector segment** — heavier, higher-displacement, higher-horsepower
  vehicles with a high share of 8-cylinder cars; smaller but commercially valuable,
  concentrated in earlier model years. Position around V8 heritage and collectability.

The recommendation is two merchandising templates and brand-aware messaging rather than
treating all vintage inventory as a single market.

## Files

- `vehicle_segmentation_pca_tsne.ipynb` — full analysis with code and outputs

## ⚠️ Before publishing: regenerate the plots

The source export this notebook was rebuilt from **did not contain rendered plot
images**, so the notebook currently shows code and text but no inline charts. Open the
notebook, run all cells top to bottom (Kernel → Restart & Run All) with `auto-mpg.csv`
in the path the notebook expects, and re-save so the visualizations render inline before
pushing to GitHub. The plots this notebook produces include: cylinder/era/brand counts,
a correlation heatmap, the PCA 2-D projection, the t-SNE projection, and the
segment scatter/box plots.

## Tools

Python · pandas · scikit-learn · matplotlib

## Notes

Auto MPG is a well-known public dataset. The business framing (SecondLife dealership) is
a scenario used to structure the analysis.
