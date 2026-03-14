resource "kubernetes_namespace" "farming" {
  metadata {
    name = "farming-platform"
  }
}

resource "kubernetes_secret" "db_secrets" {
  metadata {
    name      = "db-secrets"
    namespace = kubernetes_namespace.farming.metadata[0].name
  }

  data = {
    username = "admin"
    password = "super-secure-password"
    dbname   = "farming_db"
  }

  type = "Opaque"
}