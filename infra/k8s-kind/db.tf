resource "kubernetes_service" "postgres_service" {
  metadata {
    name      = "postgres-service"
    namespace = kubernetes_namespace.farming.metadata[0].name
  }
  spec {
    selector = {
      tier = "db"
    }
    port {
      port        = 5432
      target_port = 5432
    }
  }
}

resource "kubernetes_deployment" "postgres" {
  metadata {
    name      = "postgres-db"
    namespace = kubernetes_namespace.farming.metadata[0].name
  }
  spec {
    selector { match_labels = { tier = "db" } }
    template {
      metadata { labels = { tier = "db" } }
      spec {
        container {
          name  = "postgres"
          image = "postgres:16-alpine"
          env {
            name  = "POSTGRES_DB"
            value = "farming_db"
          }
          env {
            name  = "POSTGRES_PASSWORD"
            value = "super-secure-password"
          }
          env {
            name  = "POSTGRES_USER"
            value = "admin"
          }
        }
      }
    }
  }
}