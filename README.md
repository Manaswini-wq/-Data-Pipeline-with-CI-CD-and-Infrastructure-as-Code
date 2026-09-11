# Production Data Pipeline with CI/CD

End-to-end e-commerce data pipeline with dbt transformations, data quality
monitoring, Slack alerting, Airflow orchestration, and full CI/CD — deployed
to GCP via Terraform.

## Architecture

```
GitHub PR → CI (Lint + Test + Build)
GitHub Push (main) → CD (Terraform → Docker → dbt → Quality Checks)
Daily Schedule → Airflow DAG (Ingest → dbt → Quality → Slack Alert)
```

## Tech Stack

| Component        | Technology                    |
|------------------|-------------------------------|
| Orchestration    | Apache Airflow (Cloud Composer) |
| Transformation   | dbt (BigQuery)                |
| Data Quality     | Great Expectations + custom   |
| Alerting         | Slack SDK                     |
| Infrastructure   | Terraform                     |
| CI/CD            | GitHub Actions                |
| Warehouse        | Google BigQuery               |
| Containers       | Docker, Docker Compose        |

## Quick Start

```bash
make all           # lint + test + build
make dbt-run       # run dbt models
make quality       # run data quality checks
make deploy-infra  # provision GCP resources
```
