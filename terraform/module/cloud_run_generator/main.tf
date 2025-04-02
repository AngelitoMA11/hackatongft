resource "google_artifact_registry_repository" "repo" {
  project       = var.project_id
  location      = var.region
  repository_id = var.repository_name
  format        = "DOCKER"
}

# Autenticación con Artifact Registry
resource "null_resource" "docker_auth" {
  provisioner "local-exec" {
    command = "gcloud auth configure-docker ${var.region}-docker.pkg.dev"
  }

  depends_on = [google_artifact_registry_repository.repo]
}

# Construcción de la imagen con Docker y push a Artifact Registry
resource "null_resource" "build_push_image" {
  provisioner "local-exec" {
    command = <<EOT
      docker build --platform=linux/amd64 -t ${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_name}/${var.image_name}:latest ${path.module} && docker push ${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_name}/${var.image_name}:latest
    EOT
  }

  depends_on = [null_resource.docker_auth]
}

resource "google_cloud_run_service" "service" {
  name     = var.cloud_run_service_name
  location = var.region
  project  = var.project_id
  
  template {
    spec {
      containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_name}/${var.image_name}:latest"

      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }

      env {
        name  = "GCP_TOPIC_ID"
        value = var.topic_wifi
      }

        env {
          name  = "PORT"
          value = "8080"
        }

        ports {
          container_port = 8080
        }
    }
  }
}

  traffic {
    percent = 100
    latest_revision = true
  }
}


# Permitir acceso público
resource "google_cloud_run_service_iam_member" "invoker" {
  project  = var.project_id
  location = var.region
  service  = google_cloud_run_service.service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}