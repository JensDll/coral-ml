add_executable(coral-app src/main.cpp)

target_link_libraries(
  coral-app PRIVATE
  coral-app-servers
  coral-app-core
)
