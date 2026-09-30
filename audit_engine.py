import json
import pandas as pd


class FinancialAuditEngine:

    def __init__(self, filepath: str):
        self.df = pd.read_csv(filepath)
        self.df["posting_date"] = pd.to_datetime(self.df["posting_date"])
        self.anomalies = []

    def check_duplicates(self):
        duplicates = self.df[
            self.df.duplicated(subset=["vendor_id", "invoice_number"], keep=False)
        ]
        for _, row in duplicates.iterrows():
            self.anomalies.append(
                {
                    "transaction_id": row["transaction_id"],
                    "rule_failed": "DUPLICATE_INVOICE",
                    "severity": "HIGH",
                    "risk_amount_usd": row["total_amount"],
                    "description": f"Duplicate invoice {row['invoice_number']} for vendor {row['vendor_id']}",
                }
            )

    def check_tax_reconciliation(self, tolerance: float = 0.02):
        expected_tax = self.df["net_amount"] * self.df["tax_rate"]
        tax_diff = (self.df["tax_amount"] - expected_tax).abs()
        failed = self.df[tax_diff > tolerance]

        for _, row in failed.iterrows():
            self.anomalies.append(
                {
                    "transaction_id": row["transaction_id"],
                    "rule_failed": "TAX_CALCULATION_MISMATCH",
                    "severity": "MEDIUM",
                    "risk_amount_usd": row["tax_amount"],
                    "description": "Tax calculation discrepancy detected",
                }
            )

    def check_missing_metadata(self):
        missing = self.df[
            self.df["vendor_id"].isna() | self.df["gl_account"].isna()
        ]
        for _, row in missing.iterrows():
            self.anomalies.append(
                {
                    "transaction_id": row["transaction_id"],
                    "rule_failed": "MISSING_CRITICAL_METADATA",
                    "severity": "HIGH",
                    "risk_amount_usd": row["total_amount"],
                    "description": "Missing Vendor ID or GL Account mapping",
                }
            )

    def check_date_cutoff(self, max_date: str = "2026-12-31"):
        future = self.df[self.df["posting_date"] > pd.to_datetime(max_date)]
        for _, row in future.iterrows():
            self.anomalies.append(
                {
                    "transaction_id": row["transaction_id"],
                    "rule_failed": "PERIOD_CUTOFF_FUTURE_DATE",
                    "severity": "MEDIUM",
                    "risk_amount_usd": row["total_amount"],
                    "description": f"Future posting date: {row['posting_date'].strftime('%Y-%m-%d')}",
                }
            )

    def check_outliers(self, threshold_std: float = 3.0):
        mean_amt = self.df["net_amount"].mean()
        std_amt = self.df["net_amount"].std()
        outliers = self.df[self.df["net_amount"] > (mean_amt + threshold_std * std_amt)]

        for _, row in outliers.iterrows():
            self.anomalies.append(
                {
                    "transaction_id": row["transaction_id"],
                    "rule_failed": "MATERIAL_AMOUNT_OUTLIER",
                    "severity": "CRITICAL",
                    "risk_amount_usd": row["total_amount"],
                    "description": f"Material outlier amount: ${row['net_amount']:,.2f}",
                }
            )

    def run_pipeline(self):
        self.check_duplicates()
        self.check_tax_reconciliation()
        self.check_missing_metadata()
        self.check_date_cutoff()
        self.check_outliers()

        anomaly_df = pd.DataFrame(self.anomalies)

        flagged_tx_ids = set(anomaly_df["transaction_id"].unique()) if not anomaly_df.empty else set()
        self.df["is_flagged"] = self.df["transaction_id"].isin(flagged_tx_ids)

        total_records = len(self.df)
        clean_records = total_records - len(flagged_tx_ids)
        quality_score = round((clean_records / total_records) * 100, 2)
        total_risk_usd = (
            round(anomaly_df["risk_amount_usd"].sum(), 2)
            if not anomaly_df.empty
            else 0.0
        )

        metrics = {
            "total_records_processed": total_records,
            "flagged_transactions_count": len(flagged_tx_ids),
            "data_quality_score_percent": quality_score,
            "total_risk_exposure_usd": total_risk_usd,
        }

        self.df.to_csv("cleaned_transactions.csv", index=False)
        anomaly_df.to_csv("audit_anomaly_log.csv", index=False)
        with open("pipeline_metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)

        print("\n=== PIPELINE EXECUTION SUMMARY ===")
        for k, v in metrics.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    engine = FinancialAuditEngine("raw_financial_transactions.csv")
    engine.run_pipeline()