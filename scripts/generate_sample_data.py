import random
import csv
from datetime import datetime, timedelta

random.seed(7)

CARD_CATEGORIES = ["Blue", "Gold", "Platinum", "Silver"]
CUSTOMER_JOBS = ["Businessman", "White-collar", "Selfemployed", "Govt", "Blue-collar", "Retirees"]
EDU_LEVELS = ["Graduate", "High School", "Unknown", "Uneducated", "Post-Graduate", "Doctorate"]
USE_CHIP = ["Swipe", "Chip", "Online"]
EXP_TYPES = ["Bills", "Entertainment", "Fuel", "Grocery", "Food", "Travel"]
INCOME_GROUPS = ["Low", "Med", "High"]
GENDERS = ["F", "M"]
AGE_GROUPS = ["20-30", "30-40", "40-50", "50-60", "60+"]
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def quarter_from_month(m: int) -> str:
    if m in [1,2,3]: return "Q1"
    if m in [4,5,6]: return "Q2"
    if m in [7,8,9]: return "Q3"
    return "Q4"

def gen_transactions(n=5000, start_date="2023-01-01"):
    start = datetime.fromisoformat(start_date)
    rows = []
    for i in range(1, n+1):
        d = start + timedelta(days=random.randint(0, 364))
        month = MONTHS[d.month-1]
        qtr = quarter_from_month(d.month)

        card = random.choices(CARD_CATEGORIES, weights=[70,10,10,10])[0]
        job = random.choice(CUSTOMER_JOBS)
        edu = random.choice(EDU_LEVELS)
        chip = random.choices(USE_CHIP, weights=[63,31,6])[0]
        exp = random.choices(EXP_TYPES, weights=[28,19,18,16,13,6])[0]
        inc = random.choice(INCOME_GROUPS)
        g = random.choice(GENDERS)
        age = random.choices(AGE_GROUPS, weights=[10,20,35,25,10])[0]

        total_amt = round(random.uniform(20, 2500), 2)
        revenue = round(total_amt * random.uniform(0.01, 0.06), 2)
        interest = round(total_amt * random.uniform(0.0, 0.03), 2)
        fees = round(random.choice([0, 0, 0, 49, 99, 199]), 2)
        trans_count = random.randint(1, 5)

        rows.append({
            "transaction_id": f"T{i:07d}",
            "date": d.date().isoformat(),
            "card_category": card,
            "revenue": revenue,
            "interest_earned": interest,
            "total_trans_amt": total_amt,
            "annual_fees": fees,
            "total_trans_count": trans_count,
            "customer_job": job,
            "education_level": edu,
            "use_chip": chip,
            "exp_type": exp,
            "quarter": qtr,
            "month": month,
            "gender": g,
            "age_group": age,
            "income_group": inc,
        })
    return rows

def gen_customers(n=2000):
    rows = []
    states = ["TX","NY","CA","FL","NJ","IL","PA","GA","NC","MI"]
    marital = ["Single","Married","Unknown"]
    for i in range(1, n+1):
        g = random.choice(GENDERS)
        age = random.choices(AGE_GROUPS, weights=[10,20,35,25,10])[0]
        inc = random.choice(INCOME_GROUPS)
        edu = random.choice(EDU_LEVELS)
        job = random.choice(CUSTOMER_JOBS)
        st = random.choice(states)
        mar = random.choice(marital)
        income = round(random.uniform(15000, 250000), 2)
        sat = round(random.uniform(1.0, 5.0), 2)

        rows.append({
            "customer_id": f"C{i:06d}",
            "gender": g,
            "age_group": age,
            "income_group": inc,
            "education_level": edu,
            "marital_status": mar,
            "state": st,
            "customer_job": job,
            "total_income": income,
            "cust_satisfaction_score": sat,
        })
    return rows

def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

if __name__ == "__main__":
    tx = gen_transactions()
    cs = gen_customers()
    write_csv("data/credit_card_transactions.csv", tx)
    write_csv("data/credit_card_customers.csv", cs)
    print("✅ Generated CSV files in data/")