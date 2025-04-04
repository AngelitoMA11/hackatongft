terraform {
  backend "gcs" {
    bucket  = "mi-bucket-terraform-state"
    prefix  = "terraform/state"
  }
}

module "pubsub" {
  source         = "./module/pubsub"
  project_id     = var.project_id
  pubsub_topics  = [
    { topic_name = var.topic_wifi , subscription_name = var.sub_wifi }
  ]
}

module "bigquery" {
  source     = "./module/bigquery"
  project_id = var.project_id
  bq_dataset = var.bq_dataset
  tables = [
    { name = "wifi", schema = "module/bigquery/schemas/wifi.json" }
  ]
}

module "cloud_run_generator" {
  source             = "./module/cloud_run_generator"
  project_id         = var.project_id
  region             = var.region
  cloud_run_service_name = var.cloud_run_service_api
  repository_name    = var.repository_name_api
  image_name         = var.image_name_api
  topic_wifi         = var.topic_wifi
}

# module "cloud_run_2" {
#   source             = "./module/cloud_run_2"
#   project_id         = var.project_id
#   region             = var.region
#   cloud_run_service_name = var.cloud_run_service_api_2
#   repository_name    = var.repository_name_api_2
#   image_name         = var.image_name_api_2
#   topic_wifi         = var.topic_wifi
# }