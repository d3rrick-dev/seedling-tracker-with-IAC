variable "db_user" {
  type    = string
  default = "admin"
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "db_name" {
  type    = string
  default = "farming_db"
}

variable "app_image" {
  type    = string
  default = "seedling-api:latest"
}