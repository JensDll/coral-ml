#include "video-server.hpp"

app_servers::VideoServer::VideoServer(const app_core::Config& config,
                                      zmq::context_t& zmqContext,
                                      cv::VideoCapture& cap, int camIdx)
    : _cap{ cap }, _zmqContext{ zmqContext } {
  if (!cap.isOpened()) {
    cap.open(camIdx);
  }
  _capProps.frameWidth = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH));
  _capProps.frameHeight = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
}

void app_servers::VideoServer::start(
    app_servers::OnFrameCallback callback) const {
  cv::Mat image;

  for (int i{ 0 };; ++i) {
    _cap.read(image);
    cv::cvtColor(image, image, cv::COLOR_BGR2RGB);
    callback(image);
  }
}