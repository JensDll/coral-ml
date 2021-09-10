add_library(
  coral-app-servers
  "src/video-server.cpp"
  "include/video-server.hpp"
)

target_link_libraries(
  coral-app-servers PUBLIC
  libav libzmq opencv
)

target_include_directories(
  coral-app-servers PUBLIC
  "${CMAKE_CURRENT_SOURCE_DIR}/include"
  "${PROJECT_SOURCE_DIR}/modules/core/include"
)