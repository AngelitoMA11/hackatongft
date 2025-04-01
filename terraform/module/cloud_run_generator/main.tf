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

resource "google_cloud_run_v2_job" "job" {
  name     = var.cloud_run_job_name
  location = var.region
  project  = var.project_id

  template {
    template {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_name}/${var.image_name}:latest"
        
      }
    }
  }
  deletion_protection = false
  # depends_on = [null_resource.build_push_image]
}
