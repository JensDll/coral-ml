variable "REPOSITORY" {
  default = "jensdll/coral-ml"
}

variable "TAG" {
  default = ""
}

group "default" {
    targets = [
      "mariadb",
      "record-api",
      "node-api",
      "node-video",
      "vue-app",
      "coral-app",
      "proxy"
    ]
}

target "mariadb" {
    context = "services/mariadb"
    tags = [
      "${REPOSITORY}:mariadb_latest",
      notequal("", TAG) ? "${REPOSITORY}:mariadb_${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "record-api" {
    context = "services/record-api"
    tags = [
      "${REPOSITORY}:record-api_latest",
      notequal("", TAG) ? "${REPOSITORY}:record-api_${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "node-api" {
    context = "services/node-api"
    tags = [
      "${REPOSITORY}:node-api_latest",
      notequal("", TAG) ? "${REPOSITORY}:node-api_${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "node-video" {
    context = "services/node-video"
    tags = [
      "${REPOSITORY}:node-video_latest",
      notequal("", TAG) ? "${REPOSITORY}:node-video_${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "vue-app" {
    context = "services/vue-app"
    tags = [
      "${REPOSITORY}:vue-app_latest",
      notequal("", TAG) ? "${REPOSITORY}:vue-app_${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "coral-app" {
    context = "services/coral-app"
    tags = [
      "${REPOSITORY}:coral-app_latest",
      notequal("", TAG) ? "${REPOSITORY}:coral-app_${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "proxy" {
    context = "services/proxy"
    tags = [
      "${REPOSITORY}:proxy_latest",
      notequal("", TAG) ? "${REPOSITORY}:proxy_${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}
