variable "instance_name" {
  description = "Nombre de la instancia de PostgreSQL"
  type        = string
}

variable "region" {
  description = "Región de despliegue"
  type        = string
}

variable "instance_tier" {
  description = "Tipo de instancia (ej. db-f1-micro, db-custom-1-3840)"
  type        = string
}

variable "db_name" {
  description = "Nombre de la base de datos"
  type        = string
}

variable "db_user" {
  description = "Usuario de la base de datos"
  type        = string
}

variable "db_password" {
  description = "Contraseña del usuario"
  type        = string
  sensitive   = true
}
