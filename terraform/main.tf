module "pubsub" {
  source         = "./module/pubsub"
  project_id     = var.project_id
  pubsub_topics  = [
    { topic_name = var.topic_wifi , subscription_name = var.sub_wifi }
  ]
}

# module "bigquery" {
#   source     = "./module/bigquery"
#   project_id = var.project_id
#   bq_dataset = var.bq_dataset
  
# }
