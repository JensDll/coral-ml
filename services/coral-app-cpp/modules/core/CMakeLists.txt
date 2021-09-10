add_library(
  coral-app-core
  "src/core.cpp"
  "src/fps.cpp"
  "include/core.hpp"
)

target_link_libraries(
  coral-app-core PUBLIC
  libav libzmq opencv
)

target_include_directories(
  coral-app-core PUBLIC
  "${CMAKE_CURRENT_SOURCE_DIR}/include"
)