add_library(
  zmq-servers
  src/zmq-servers.hpp
  src/video-server.cpp
)

target_include_directories(
  zmq-servers PUBLIC
  "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

target_include_directories(
  zmq-servers PUBLIC
  "${PROJECT_SOURCE_DIR}"
)
