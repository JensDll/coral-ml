#include <iostream>
#include <opencv2/opencv.hpp>
#include <string>
#include <thread>
#include <zmq.hpp>

#include "servers.hpp"

int main(int argc, char **argv) {
  zmq::context_t context{1};

  cv::VideoCapture cap{};
  cap.open(0);

  if (!cap.isOpened()) {
    return EXIT_FAILURE;
  }

  servers::VideoServer video_server{cap, context};
  std::thread video_server_thread{&servers::VideoServer::start, video_server};
  video_server_thread.join();

  return EXIT_SUCCESS;
}
