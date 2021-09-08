#include <opencv2/opencv.hpp>
#include <string>
#include <zmq.hpp>

#include "core.hpp"

#ifndef CORAL_APP_VIDEO_SERVER
#define CORAL_APP_VIDEO_SERVER
namespace app_servers {

using OnFrameCallback = void (*)(const cv::Mat& frame);

class VideoServer {
 public:
  VideoServer(const app_core::Config& config, zmq::context_t& context,
              cv::VideoCapture& cap, int camIdx = 0);

  void start(OnFrameCallback callback) const;

 private:
  cv::VideoCapture& _cap;
  zmq::context_t& _zmqContext;
  struct CapProps {
    int frameWidth;
    int frameHeight;
  } _capProps;
};

}  // namespace app_servers
#endif