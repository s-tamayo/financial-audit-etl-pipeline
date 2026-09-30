import numpy as np
import pandas as pd

np.random.seed(42)
n_records = 1000

vendors = [f"VEND-{i:03d}" for i in range(1, 26)]
gl_accounts = [1010, 1200, 2000, 4000, 5000, 6100, 6200, 7000]
dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")

df = pd.DataFrame(
    {
        "transaction_id": [f"TXN-{10000 + i}" for i in range(n_records)],
        "posting_date": np.random.choice(dates, n_records),
        "vendor_id": np.random.choice(vendors, n_records),
        "invoice_number": [
            f"INV-{np.random.randint(10000, 99999)}" for _ in range(n_records)
        ],
        "gl_account": np.random.choice(gl_accounts, n_records),
        "net_amount": np.round(np.random.uniform(50.0, 15000.0, n_records), 2),
        "tax_rate": 0.0825,
        "approval_status": np.random.choice(
            ["APPROVED", "PENDING", "REJECTED"], n_records, p=[0.85, 0.10, 0.05]
        ),
    }
)

df["tax_amount"] = np.round(df["net_amount"] * df["tax_rate"], 2)
df["total_amount"] = df["net_amount"] + df["tax_amount"]

# Inject Synthetic Audit Anomalies
df.loc[10:15, "invoice_number"] = df.loc[0:5, "invoice_number"].values
df.loc[10:15, "vendor_id"] = df.loc[0:5, "vendor_id"].values

df.loc[50:60, "tax_amount"] = df.loc[50:60, "tax_amount"] * 1.5
df.loc[50:60, "total_amount"] = (
    df.loc[50:60, "net_amount"] + df.loc[50:60, "tax_amount"]
)

df.loc[100:110, "vendor_id"] = np.nan

df.loc[200:203, "net_amount"] = [250000.00, 500000.00, 1200000.00, 850000.00]
df.loc[200:203, "total_amount"] = df.loc[200:203, "net_amount"] * 1.0825

df.loc[300:305, "posting_date"] = pd.to_datetime("2027-06-15")

df.to_csv("raw_financial_transactions.csv", index=False)
print("SUCCESS: Generated raw_financial_transactions.csv (1,000 records).")