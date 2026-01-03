import pandas as pd
from pathlib import Path

TX_PATH = Path("data/credit_card_transactions.csv")
CS_PATH = Path("data/credit_card_customers.csv")

def must_have_columns(df, cols, name):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"{name}: missing columns: {missing}")

def main():
    tx = pd.read_csv(TX_PATH)
    cs = pd.read_csv(CS_PATH)

    must_have_columns(tx, ["transaction_id","date","card_category","revenue","total_trans_amt","total_trans_count"], "transactions")
    must_have_columns(cs, ["customer_id","gender","age_group","income_group","total_income","cust_satisfaction_score"], "customers")

    # Basic checks
    assert tx["transaction_id"].isna().sum() == 0
    assert cs["customer_id"].isna().sum() == 0
    assert (tx["revenue"] >= 0).all()
    assert (tx["total_trans_amt"] > 0).all()
    assert cs["cust_satisfaction_score"].between(1.0, 5.0).all()

    print("✅ Validation passed")
    print(f"Transactions: {len(tx):,} rows | Customers: {len(cs):,} rows")

if __name__ == "__main__":
    main()
