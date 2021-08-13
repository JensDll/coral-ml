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
      "${REPOSITORY}:mariadb.latest",
      notequal("", TAG) ? "${REPOSITORY}:mariadb.${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "record-api" {
    context = "services/record-api"
    tags = [
      "${REPOSITORY}:record-api.latest",
      notequal("", TAG) ? "${REPOSITORY}:record-api.${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "node-api" {
    context = "services/node-api"
    tags = [
      "${REPOSITORY}:node-api.latest",
      notequal("", TAG) ? "${REPOSITORY}:node-api.${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "node-video" {
    context = "services/node-video"
    tags = [
      "${REPOSITORY}:node-video.latest",
      notequal("", TAG) ? "${REPOSITORY}:node-video.${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "vue-app" {
    context = "services/vue-app"
    tags = [
      "${REPOSITORY}:vue-app.latest",
      notequal("", TAG) ? "${REPOSITORY}:vue-app.${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "coral-app" {
    context = "services/coral-app"
    tags = [
      "${REPOSITORY}:coral-app.latest",
      notequal("", TAG) ? "${REPOSITORY}:coral-app.${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}

target "proxy" {
    context = "services/proxy"
    tags = [
      "${REPOSITORY}:proxy.latest",
      notequal("", TAG) ? "${REPOSITORY}:proxy.${TAG}" : ""
    ]
    platforms = [
      "linux/amd64",
      "linux/arm64"
    ]
}