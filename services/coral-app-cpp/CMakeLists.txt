cmake_minimum_required(VERSION 3.0.0)
project(coralapp VERSION 0.1.0)

include(CTest)
enable_testing()

add_executable(coralapp main.cpp)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)

if (WIN32)
  target_link_libraries(coralapp -llibzmq)
else ()
  find_package(cppzmq REQUIRED)
  target_link_libraries(coralapp cppzmq)
endif (WIN32)

find_package(
  OpenCV
  REQUIRED
  PATH_SUFFIXES /install/lib/cmake/opencv4
)
include_directories(${OpenCV_INCLUDE_DIRS})
target_link_libraries(coralapp ${OpenCV_LIBS})

add_subdirectory(servers)
target_link_libraries(coralapp coral-app-servers)
target_include_directories(
  coralapp PUBLIC
  "${PROJECT_BINARY_DIR}"
  "${PROJECT_SOURCE_DIR}/servers"
)