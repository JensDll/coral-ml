#include <opencv2/opencv.hpp>
#include <string>
#include <zmq.hpp>

#include "main.hpp"

#ifndef CORAL_APP_VIDEO_SERVER
#define CORAL_APP_VIDEO_SERVER
namespace zmq_servers {

class VideoServer {
 public:
  VideoServer(cv::VideoCapture& cap, zmq::context_t& context);

  void start(const coral_app_main::Config& config) const;

 private:
  cv::VideoCapture& m_cap;
  zmq::context_t& m_context;
  const struct CapProps {
    int frame_width;
    int frame_height;
  } m_cap_props;

  std::string build_ffmpeg_command(const coral_app_main::Config& config) const;
};

}  // namespace zmq_servers
#endif