#include <opencv2/opencv.hpp>
#include <zmq.hpp>

#ifndef CORAL_APP_SERVERS
#define CORAL_APP_SERVERS
namespace servers {
class VideoServer {
 public:
  VideoServer(cv::VideoCapture &cap, zmq::context_t &context);
  void start();

 private:
  cv::VideoCapture &cap;
  zmq::context_t &context;
  struct cap_props_s {
    int frame_width;
    int frame_height;
  } cap_props;
};
}  // namespace servers
#endif