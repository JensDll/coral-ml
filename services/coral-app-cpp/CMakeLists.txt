cmake_minimum_required(VERSION 3.0.0)
project(CoralApp VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_subdirectory(lib/libav)
add_subdirectory(lib/libzmq)
add_subdirectory(lib/opencv)

add_subdirectory(modules/core)
add_subdirectory(modules/servers)
add_subdirectory(modules/main-exe)
