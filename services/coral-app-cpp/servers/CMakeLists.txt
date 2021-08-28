add_library(coral-app-servers video-server.cpp)

install(
  TARGETS
    coral-app-servers
  DESTINATION lib
)
install(
  FILES
    servers.hpp
  DESTINATION include
)