resource "kubernetes_deployment" "api" {
  metadata {
    name      = "seedling-api"
    namespace = kubernetes_namespace.farming.metadata[0].name
    labels    = { app = "seedling-api" }
    annotations = {
      # force a restart run apply
      "redeploy-timestamp" = "${timestamp()}"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = { app = "seedling-api" }
    }

    template {
      metadata {
        labels = { app = "seedling-api" }
      }

      spec {
        container {
          image = "seedling-api:v3"
          name  = "api"
          
          #fon't try to pull from Docker Hub
          image_pull_policy = "Never" # prod -> Always, IfNotPresent

          port { container_port = 8000 }

          # is the app dead? (If so, restart it)
          liveness_probe {
            http_get {
              path = "/docs"
              port = 8000
            }
            initial_delay_seconds = 20
            period_seconds        = 10
          }

          # is the app ready to take traffic?
          readiness_probe {
            http_get {
              path = "/docs"
              port = 8000
            }
            initial_delay_seconds = 20
            period_seconds        = 5
          }

          env {
            name  = "DB_HOST"
            value = "host.docker.internal" 
          }

          env {
            name = "DB_PASS"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.db_secrets.metadata[0].name
                key  = "password"
              }
            }
          }
          env {
            name  = "DATABASE_URL"
            value = "postgresql://postgres:password@host.docker.internal:4510/seedling_db"
          }
          env {
            name  = "S3_ENDPOINT"
            value = "http://host.docker.internal:4566"
          }
          env {
            name  = "S3_BUCKET"
            value = "seedling-assets"
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "api_service" {
  metadata {
    name      = "api-service"
    namespace = kubernetes_namespace.farming.metadata[0].name
  }
  spec {
    selector = { app = "seedling-api" }
    port {
      port        = 80
      target_port = 8000
    }
    type = "NodePort"
  }
}

// a worker for generating thumbnails
resource "kubernetes_deployment" "worker" {
  metadata {
    name      = "seedling-worker"
    namespace = kubernetes_namespace.farming.metadata[0].name
    annotations = {
      "redeploy-timestamp" = "${timestamp()}"
    }
  }
  spec {
    replicas = 1
    selector { match_labels = { app = "seedling-worker" } }
    template {
      metadata { labels = { app = "seedling-worker" } }
      spec {
        container {
          name  = "worker"
          image = "seedling-api:v3"
          image_pull_policy = "Never"
          command = ["python"]
          args    = ["-m", "app.worker"]

          env {
            name  = "DATABASE_URL"
            value = "postgresql://postgres:password@host.docker.internal:4510/seedling_db"
          }
          env_from {
            secret_ref {
              name = kubernetes_secret.db_secrets.metadata[0].name
            }
          }
          env {
            name  = "S3_ENDPOINT"
            value = "http://host.docker.internal:4566"
          }
          env {
            name  = "S3_BUCKET"
            value = "seedling-assets"
          }
          env {
            name  = "SQS_QUEUE_URL"
            value = "http://host.docker.internal:4566/000000000000/plant-photo-processing"
          }
        }
      }
    }
  }
}