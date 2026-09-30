# Financial Audit & Data Quality Validation ETL Pipeline

An automated financial data quality engine and ETL pipeline built with **Python** and **Pandas**. This project ingests raw General Ledger (GL) and vendor transaction datasets, executes automated accounting integrity checks, flags compliance anomalies, and generates audit risk metrics.

---

## Technical Architecture

[ Raw Financial Data ] ──> [ Python Audit Engine ] ──> [ Data Quality Outputs ]

Invoices & Batches       - Duplicate Detection       - Cleaned Ledger CSV

Vendor Master Data       - Tax Math Reconciliation   - Anomaly Log CSV

GL Line Items            - Period Cutoff Checks      - Metrics JSON
- Outlier (3-Sigma) Flags

---

## Audit Rules & Validation Engine

| Rule ID | Anomaly Check | Severity Level | Business Impact |
| :--- | :--- | :--- | :--- |
| `DUPLICATE_INVOICE` | Identifies identical invoice numbers for the same vendor | **HIGH** | Prevents double-payment & fraud exposure |
| `TAX_CALCULATION_MISMATCH` | Recalculates line-item tax against tax rate thresholds | **MEDIUM** | Ensures tax compliance & GL accuracy |
| `MISSING_CRITICAL_METADATA` | Detects unassigned vendor IDs or missing GL account mappings | **HIGH** | Ensures reporting completeness |
| `PERIOD_CUTOFF_FUTURE_DATE` | Flags transactions posted beyond the current accounting period | **MEDIUM** | Enforces accrual/cutoff accounting principles |
| `MATERIAL_AMOUNT_OUTLIER` | Flags transactions > 3 standard deviations from the dataset mean | **CRITICAL** | Isolates material audit risks |

---

## Repository Structure

financial-audit-etl-pipeline/
├── generate_data.py             # Generates synthetic transactional dataset with injected audit anomalies
├── audit_engine.py              # Core Python data engine running validation rules and logging risk flags
├── raw_financial_transactions.csv# Generated raw input data (1,000 GL line items)
├── cleaned_transactions.csv     # Validated dataset with boolean flags
├── audit_anomaly_log.csv        # Detailed audit trail logging rule failures, severity, and dollar risk
├── pipeline_metrics.json        # High-level pipeline execution summary metrics
├── LICENSE                      # MIT License
└── README.md                    # Documentation

---

## Getting Started

### Prerequisites
* Python 3.10+
* `pandas` and `numpy`

### Installation & Run
```powershell
# Clone the repository
git clone [https://github.com/s-tamayo/financial-audit-etl-pipeline.git](https://github.com/s-tamayo/financial-audit-etl-pipeline.git)
cd financial-audit-etl-pipeline

# Install dependencies
pip install pandas numpy

# Generate synthetic dataset
python generate_data.py

# Run audit validation pipeline
python audit_engine.py

---

### Step 4: Run the Engine & Push to GitHub

Run these commands in your VS Code terminal to execute the scripts and push your updated files to GitHub:

```powershell
python generate_data.py
python audit_engine.py
git add .
git commit -m "Add synthetic data generator, audit engine, outputs, and documentation"
git push