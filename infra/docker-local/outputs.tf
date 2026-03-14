output "swagger_url" {
  value       = "http://localhost:8000/docs"
  description = "The URL to access your Farming API documentation"
}

output "database_host" {
  value       = docker_container.postgres_db.name
  description = "The hostname for the database"
}