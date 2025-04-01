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
  
}

module "cloud_run_generator" {
  source             = "./module/cloud_run_generator"
  project_id         = var.project_id
  region             = var.region
  cloud_run_job_name = var.cloud_run_job_api
  repository_name    = var.repository_name_api
  image_name         = var.image_name_api
  topic_wifi         = var.topic_wifi
}
