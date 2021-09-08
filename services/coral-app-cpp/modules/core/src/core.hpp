#include <string>

#ifndef CORAL_APP_MAIN
#define CORAL_APP_MAIN
namespace app_core {

struct Config {
  const std::string publish_uri;
  const std::string api_uri;
  const std::string loglevel;
};

}  // namespace app_core
#endif

#ifdef av_err2str
#undef av_err2str
inline std::string av_err2string(int errorNumber) {
  char str[AV_ERROR_MAX_STRING_SIZE];
  return av_make_error_string(str, AV_ERROR_MAX_STRING_SIZE, errorNumber);
}
#define av_err2str(err) av_err2string(err).c_str()
#endif