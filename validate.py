"""Reproduce the source-data checks for the Power BI report."""
import json
from pathlib import Path

import pandas as pd

source = Path(__file__).parent / "Kevin Cookie Company Orders Power BI 10 minutes.xlsx"
orders = pd.read_excel(source, sheet_name="Orders")
customers = pd.read_excel(source, sheet_name="Customers")
summary = {
    "orders": len(orders),
    "customers": len(customers),
    "cookies_shipped": int(orders["Cookies Shipped"].sum()),
    "revenue": int(orders["Revenue"].sum()),
    "cost": float(orders["Cost"].sum()),
    "duplicate_order_ids": int(orders["Order ID"].duplicated().sum()),
    "unmatched_customer_ids": int((~orders["Customer ID"].isin(customers["Customer ID"])).sum()),
    "missing_values": int(orders.isna().sum().sum()),
    "revenue_equals_quantity_times_5": bool((orders["Revenue"] == orders["Cookies Shipped"] * 5).all()),
}
assert customers["Customer ID"].is_unique, "Customer IDs must be unique"
assert summary["duplicate_order_ids"] == 0, "Duplicate orders found"
assert summary["unmatched_customer_ids"] == 0, "Unmatched customers found"
assert summary["missing_values"] == 0, "Missing order values found"
expected = json.loads((source.parent / "validation.json").read_text())
assert summary == expected, f"Source data differs from saved controls: {summary}"
print(json.dumps(summary, indent=2))
print("All validation checks passed.")
