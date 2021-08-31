add_library(opencv INTERFACE)

find_package(
  OpenCV
  REQUIRED
  PATH_SUFFIXES /install/lib/cmake/opencv4
)
include_directories(${OpenCV_INCLUDE_DIRS})
target_link_libraries(opencv INTERFACE ${OpenCV_LIBS})