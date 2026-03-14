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
    replicas = 2

    selector {
      match_labels = { app = "seedling-api" }
    }

    template {
      metadata {
        labels = { app = "seedling-api" }
      }

      spec {
        container {
          image = "seedling-api:latest"
          name  = "api"
          
          #Don't try to pull from Docker Hub
          image_pull_policy = "Never" # prod -> Always, IfNotPresent

          port { container_port = 8000 }

          # Is the app dead? (If so, restart it)
          liveness_probe {
            http_get {
              path = "/docs"
              port = 8000
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }

          # Readiness: Is the app ready to take traffic?
          readiness_probe {
            http_get {
              path = "/docs"
              port = 8000
            }
            initial_delay_seconds = 5
            period_seconds        = 5
          }

          env {
            name  = "DB_HOST"
            value = "postgres-service" # Internal K8s DNS name
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
        }
      }
    }
  }
}

resource "kubernetes_service" "api_service" {
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
    type = "NodePort" # Makes it accessible on your laptop
  }
}