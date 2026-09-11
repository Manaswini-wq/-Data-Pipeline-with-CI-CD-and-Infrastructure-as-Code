variable "project_id" { type = string }
variable "region" { default = "us-central1" }

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_bigquery_dataset" "raw" {
  dataset_id = "ecommerce_raw"
  location   = var.region
}

resource "google_bigquery_dataset" "analytics" {
  dataset_id = "ecommerce_analytics"
  location   = var.region
}

resource "google_bigquery_dataset" "analytics_prod" {
  dataset_id = "ecommerce_analytics_prod"
  location   = var.region
}

resource "google_storage_bucket" "pipeline" {
  name          = "${var.project_id}-pipeline-artifacts"
  location      = var.region
  force_destroy = true
}

resource "google_composer_environment" "airflow" {
  name   = "ecommerce-airflow"
  region = var.region

  config {
    software_config {
      image_version = "composer-2.6.6-airflow-2.7.3"
      pypi_packages = {
        "dbt-bigquery"          = "==1.7.7"
        "great-expectations"    = "==0.18.12"
        "slack-sdk"             = "==3.27.1"
      }
    }
    workloads_config {
      scheduler { cpu = 1; memory_gb = 2 }
      web_server { cpu = 1; memory_gb = 2 }
      worker { cpu = 2; memory_gb = 4; min_count = 1; max_count = 3 }
    }
  }
}
