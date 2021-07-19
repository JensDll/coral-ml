variable "REPOSITORY" {
  default = "jensdll/coral-ml"
}

group "default" {
    targets = [
      "mariadb",
      "record-api",
      "node-socket",
      "vue-app",
      "coral-app",
      "proxy"
    ]
}

target "mariadb" {
    context = "services/mariadb"
    tags = [
      "${REPOSITORY}:mariadb-latest"
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "record-api" {
    context = "services/record-api"
    tags = [
      "${REPOSITORY}:record-api-latest"
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "node-socket" {
    context = "services/node-socket"
    tags = [
      "${REPOSITORY}:node-socket-latest"
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "vue-app" {
    context = "services/vue-app"
    tags = [
      "${REPOSITORY}:vue-app-latest"
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "coral-app" {
    context = "services/coral-app"
    tags = [
      "${REPOSITORY}:coral-app-latest"
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "proxy" {
    context = "services/proxy"
    tags = [
      "${REPOSITORY}:proxy-latest"
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}