variable "project_id" {
  description = "ID del proyecto de GCP."
  type        = string
}
  
variable "zone" {
  description = "Zona del proyecto"
  type        = string
}

variable "topic_wifi" {
  description = "Nombre del tópico de helpers."
  type        = string
}

variable "sub_wifi" {
  description = "Nombre de la suscripción de helpers."
  type        = string
}

variable "bq_dataset" {
  description = "Nombre del dataset de BigQuery."
  type        = string
}

variable "region" {
  description = "Región de GCP donde se desplegarán los recursos."
  type        = string
}
variable "cloud_run_service_api" {
  description = "Nombre del Cloud Run Service"
  type        = string
}

variable "repository_name_api" {
  description = "Nombre del repositorio en Artifact Registry"
  type        = string
}

variable "image_name_api" {
  description = "Nombre de la imagen en Artifact Registry"
  type        = string
}

variable "wifi" {
  description = "Nombre de la tabla de BigQuery para los datos de match."
  type        = string
}

