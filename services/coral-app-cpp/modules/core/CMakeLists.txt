add_library(
  coral-app-core
  src/core.hpp
  src/core.cpp
)

target_link_libraries(
  coral-app-core PUBLIC
  libav libzmq opencv
)

target_include_directories(
  coral-app-core PUBLIC
  "${CMAKE_CURRENT_SOURCE_DIR}/src"
)