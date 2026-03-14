resource "docker_network" "farming_net" {
  name = "farming_network"
}

resource "docker_container" "postgres_db" {
  name  = "db"
  image = "postgres:16-alpine"
  
  networks_advanced {
    name = docker_network.farming_net.name
  }

  env = [
    "POSTGRES_USER=${var.db_user}",
    "POSTGRES_PASSWORD=${var.db_password}",
    "POSTGRES_DB=${var.db_name}"
  ]

  ports {
    internal = 5432
    external = 5432
  }
}

resource "docker_container" "fastapi_app" {
  name  = "seedling_app"
  image = var.app_image
  
  networks_advanced {
    name = docker_network.farming_net.name
  }

  env = [
    "DB_HOST=db",
    "DB_USER=${var.db_user}",
    "DB_PASS=${var.db_password}",
    "DB_NAME=${var.db_name}"
  ]

  ports {
    internal = 8000
    external = 8000
  }

  depends_on = [docker_container.postgres_db]
}