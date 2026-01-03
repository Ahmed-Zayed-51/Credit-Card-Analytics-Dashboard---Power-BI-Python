# Work Done (Python)

This repo includes a Python analytics layer on top of the demo CSV dataset.

## What was implemented
1. **KPI extraction** (saved to `analysis/exports/summary_kpis.json`)
2. **Aggregations / Extractions** (saved as CSVs in `analysis/exports/`)
   - Revenue by card category / job / education level
   - Chip usage share
   - Transaction counts by expense type
   - Revenue by quarter
   - Total income by income group
   - Average satisfaction by customer job
3. **Figures** (saved as PNGs in `analysis/figures/`)
   - Bar charts for key groupings
   - Pie chart for chip usage share
   - Histogram for satisfaction distribution

## How to reproduce
```bash
pip install -r requirements.txt
python analysis/run_eda.py
```
