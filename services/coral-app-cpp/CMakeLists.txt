cmake_minimum_required(VERSION 3.0.0)
project(CoralApp VERSION 0.1.0)

add_subdirectory(lib/libzmq)
add_subdirectory(lib/opencv)

add_subdirectory(modules/zmq-servers)
add_subdirectory(modules/coral-app-exe)
