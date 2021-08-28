cmake_minimum_required(VERSION 3.0.0)
project(CoralApp VERSION 0.1.0)

add_executable(coral-app main.cpp)

# ---------- Link third party libraries ----------

# Link Libzmq
if(WIN32)
  target_link_libraries(coral-app PRIVATE -llibzmq)
else()
  find_package(cppzmq REQUIRED)
  target_link_libraries(coral-app PRIVATE cppzmq)
endif()

# Link OpenCV
find_package(
  OpenCV
  REQUIRED
  PATH_SUFFIXES /install/lib/cmake/opencv4
)
include_directories(${OpenCV_INCLUDE_DIRS})
target_link_libraries(coral-app PRIVATE ${OpenCV_LIBS})

# ---------- Link local libraries ----------

add_subdirectory(zmq-servers)
target_link_libraries(coral-app PRIVATE zmq-servers)
