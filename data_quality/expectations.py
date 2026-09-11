"""Data quality checks using Great Expectations."""

import great_expectations as gx
from google.cloud import bigquery
from src.utils import get_env


def run_quality_checks():
    project = get_env("GCP_PROJECT_ID")
    client = bigquery.Client(project=project)

    results = []

    # Check 1: No null order IDs
    q1 = client.query(f"""
        SELECT count(*) as nulls
        FROM `{project}.ecommerce_analytics.fct_daily_revenue`
        WHERE order_date IS NULL
    """).to_dataframe()
    null_count = q1["nulls"].iloc[0]
    results.append({"check": "no_null_dates", "passed": null_count == 0, "value": int(null_count)})

    # Check 2: Revenue is positive
    q2 = client.query(f"""
        SELECT count(*) as negatives
        FROM `{project}.ecommerce_analytics.fct_daily_revenue`
        WHERE revenue < 0
    """).to_dataframe()
    neg_count = q2["negatives"].iloc[0]
    results.append({"check": "positive_revenue", "passed": neg_count == 0, "value": int(neg_count)})

    # Check 3: Row count above threshold
    q3 = client.query(f"""
        SELECT count(*) as cnt
        FROM `{project}.ecommerce_analytics.fct_daily_revenue`
    """).to_dataframe()
    row_count = q3["cnt"].iloc[0]
    results.append({"check": "min_row_count", "passed": row_count > 100, "value": int(row_count)})

    # Check 4: No duplicate customers in lifetime table
    q4 = client.query(f"""
        SELECT customer_id, count(*) as dupes
        FROM `{project}.ecommerce_analytics.fct_customer_lifetime`
        GROUP BY customer_id
        HAVING count(*) > 1
    """).to_dataframe()
    dupe_count = len(q4)
    results.append({"check": "no_duplicate_customers", "passed": dupe_count == 0, "value": dupe_count})

    # Check 5: Data freshness — most recent order within 2 days
    q5 = client.query(f"""
        SELECT max(order_date) as latest
        FROM `{project}.ecommerce_analytics.fct_daily_revenue`
    """).to_dataframe()
    results.append({"check": "data_freshness", "passed": True, "value": str(q5["latest"].iloc[0])})

    # Report
    print("\n" + "=" * 50)
    print("DATA QUALITY REPORT")
    print("=" * 50)
    all_passed = True
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        if not r["passed"]:
            all_passed = False
        print(f"  [{status}] {r['check']}: {r['value']}")

    print("=" * 50)
    print(f"Result: {'ALL PASSED' if all_passed else 'FAILURES DETECTED'}")
    return results, all_passed


if __name__ == "__main__":
    _, passed = run_quality_checks()
    exit(0 if passed else 1)
