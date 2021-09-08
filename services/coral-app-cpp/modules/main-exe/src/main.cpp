#include <iostream>
#include <opencv2/opencv.hpp>
#include <string>
#include <thread>
#include <zmq.hpp>

#include "core.hpp"
#include "video-server.hpp"

void onFrame(const cv::Mat& frame) {}

int main(int argc, char** argv) {
  if (argc != 3) {
    std::cout << "Invalid number of arguments (" << argc << ")" << std::endl;
    return EXIT_FAILURE;
  }

  app_core::Config config{ std::string{ argv[1] }, std::string{ "" },
                           std::string{ argv[2] } };

  zmq::context_t context{ 1 };

  cv::VideoCapture cap;
  app_servers::VideoServer videoServer{ config, context, cap };
  std::thread videoServerThread{
    &app_servers::VideoServer::start,
    videoServer,
    onFrame,
  };
  videoServerThread.join();

  return EXIT_SUCCESS;
}