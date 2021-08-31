add_executable(coral-app main.cpp)

target_link_libraries(coral-app PRIVATE zmq-servers)