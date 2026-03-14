terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  # mac/linux, this usually defaults correctly
  # host = "unix:///var/run/docker.sock"
}