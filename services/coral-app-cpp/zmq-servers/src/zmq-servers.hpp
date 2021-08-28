#include <opencv2/opencv.hpp>
#include <string>
#include <zmq.hpp>

#include "main.hpp"

#ifndef CORAL_APP_ZMQ_SERVERS
#define CORAL_APP_ZMQ_SERVERS
namespace zmq_servers {

class VideoServer {
 public:
  VideoServer(cv::VideoCapture &cap, zmq::context_t &context);

  void start(const coral_app_main::Config config);
  void test();

 private:
  cv::VideoCapture &cap;
  zmq::context_t &context;
  struct CapProps {
    int frame_width;
    int frame_height;
  } cap_props;

  std::string build_ffmpeg_command(const coral_app_main::Config &config);
};

}  // namespace zmq_servers
#endif