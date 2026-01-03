"""
Credit Card Analytics Dashboard - Python EDA
===========================================

This script generates:
- KPI summary (JSON)
- Aggregated CSV exports (group-bys)
- Figures (PNG) for charts

Run:
  python analysis/run_eda.py
"""

from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
FIGS = BASE / "analysis" / "figures"
EXPORTS = BASE / "analysis" / "exports"

TX_PATH = DATA / "credit_card_transactions.csv"
CS_PATH = DATA / "credit_card_customers.csv"

def save_bar(df, x, y, title, filename, rotate=0):
    plt.figure(figsize=(8, 4.5))
    plt.bar(df[x].astype(str), df[y])
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    if rotate:
        plt.xticks(rotation=rotate, ha="right")
    plt.tight_layout()
    plt.savefig(FIGS / filename, dpi=160)
    plt.close()

def main():
    FIGS.mkdir(parents=True, exist_ok=True)
    EXPORTS.mkdir(parents=True, exist_ok=True)

    tx = pd.read_csv(TX_PATH)
    cs = pd.read_csv(CS_PATH)

    # KPIs
    summary = {
        "kpis": {
            "total_revenue": float(tx["revenue"].sum()),
            "total_interest": float(tx["interest_earned"].sum()),
            "total_transaction_amount": float(tx["total_trans_amt"].sum()),
            "total_annual_fees": float(tx["annual_fees"].sum()),
            "total_transaction_count": int(tx["total_trans_count"].sum()),
            "num_rows_transactions": int(len(tx)),
            "num_rows_customers": int(len(cs)),
            "avg_satisfaction": float(cs["cust_satisfaction_score"].mean()),
            "total_income": float(cs["total_income"].sum()),
        }
    }

    # Extractions / aggregations
    rev_by_card = tx.groupby("card_category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    rev_by_job = tx.groupby("customer_job", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    rev_by_edu = tx.groupby("education_level", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    chip_share = tx["use_chip"].value_counts(normalize=True).rename_axis("use_chip").reset_index(name="share")
    exp_counts = tx["exp_type"].value_counts().rename_axis("exp_type").reset_index(name="txn_count")
    qtr_rev = tx.groupby("quarter", as_index=False)["revenue"].sum().sort_values("quarter")

    income_by_group = cs.groupby("income_group", as_index=False)["total_income"].sum().sort_values("total_income", ascending=False)
    sat_by_job = cs.groupby("customer_job", as_index=False)["cust_satisfaction_score"].mean().sort_values("cust_satisfaction_score", ascending=False)

    # Save exports
    rev_by_card.to_csv(EXPORTS / "revenue_by_card_category.csv", index=False)
    rev_by_job.to_csv(EXPORTS / "revenue_by_customer_job.csv", index=False)
    rev_by_edu.to_csv(EXPORTS / "revenue_by_education_level.csv", index=False)
    chip_share.to_csv(EXPORTS / "chip_usage_share.csv", index=False)
    exp_counts.to_csv(EXPORTS / "transaction_count_by_exp_type.csv", index=False)
    qtr_rev.to_csv(EXPORTS / "revenue_by_quarter.csv", index=False)
    income_by_group.to_csv(EXPORTS / "total_income_by_income_group.csv", index=False)
    sat_by_job.to_csv(EXPORTS / "avg_satisfaction_by_job.csv", index=False)

    with open(EXPORTS / "summary_kpis.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Figures
    save_bar(rev_by_card, "card_category", "revenue", "Revenue by Card Category", "revenue_by_card_category.png")
    save_bar(rev_by_job, "customer_job", "revenue", "Revenue by Customer Job", "revenue_by_customer_job.png", rotate=20)
    save_bar(rev_by_edu, "education_level", "revenue", "Revenue by Education Level", "revenue_by_education_level.png", rotate=20)
    save_bar(exp_counts, "exp_type", "txn_count", "Transaction Count by Expense Type", "txn_count_by_exp_type.png", rotate=20)
    save_bar(qtr_rev, "quarter", "revenue", "Revenue by Quarter", "revenue_by_quarter.png")

    plt.figure(figsize=(6, 4.5))
    plt.pie(chip_share["share"], labels=chip_share["use_chip"].astype(str), autopct="%1.0f%%")
    plt.title("Chip Usage Share")
    plt.tight_layout()
    plt.savefig(FIGS / "chip_usage_share.png", dpi=160)
    plt.close()

    plt.figure(figsize=(7, 4.5))
    plt.hist(cs["cust_satisfaction_score"], bins=20)
    plt.title("Customer Satisfaction Score Distribution")
    plt.xlabel("cust_satisfaction_score")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(FIGS / "satisfaction_distribution.png", dpi=160)
    plt.close()

    print("✅ EDA complete. Outputs saved to analysis/exports and analysis/figures.")

if __name__ == "__main__":
    main()
