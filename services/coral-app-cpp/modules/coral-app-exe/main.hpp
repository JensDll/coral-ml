#include <string>

#ifndef CORAL_APP_MAIN
#define CORAL_APP_MAIN
namespace coral_app_main {

struct Config {
  std::string publish_uri;
  std::string api_uri;
  std::string loglevel;
};

}  // namespace coral_app_main
#endif