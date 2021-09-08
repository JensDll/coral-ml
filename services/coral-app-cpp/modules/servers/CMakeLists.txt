add_library(
  coral-app-servers
  src/video-server.hpp
  src/video-server.cpp
)

target_link_libraries(
  coral-app-servers PUBLIC
  libav libzmq opencv
)

target_include_directories(
  coral-app-servers PUBLIC
  "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

target_include_directories(
  coral-app-servers PUBLIC
  "${PROJECT_SOURCE_DIR}/modules/core/src"
)