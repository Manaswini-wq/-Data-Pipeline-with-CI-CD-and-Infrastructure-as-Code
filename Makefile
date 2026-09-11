.PHONY: lint test build deploy quality

lint:
	sqlfluff lint dbt_project/models/ --dialect bigquery
	python -m py_compile src/ingest.py
	python -m py_compile dags/ecommerce_pipeline.py

test:
	pytest tests/ -v

quality:
	python -m data_quality.expectations

build:
	docker build -t ecommerce-pipeline .

fmt:
	sqlfluff fix dbt_project/models/ --dialect bigquery

dbt-run:
	cd dbt_project && dbt run --profiles-dir .

dbt-test:
	cd dbt_project && dbt test --profiles-dir .

deploy-infra:
	cd terraform && terraform init && terraform apply -auto-approve

all: lint test build
