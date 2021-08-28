#include "main.hpp"

#include <iostream>
#include <opencv2/opencv.hpp>
#include <string>
#include <thread>
#include <zmq.hpp>

#include "zmq-servers.hpp"

int main(int argc, char **argv) {
  coral_app_main::Config config{};
  config.publish_uri = std::string{argv[1]};
  config.loglevel = std::string{argv[2]};

  zmq::context_t context{1};

  cv::VideoCapture cap{};
  cap.open(0);

  if (!cap.isOpened()) {
    return EXIT_FAILURE;
  }

  const zmq_servers::VideoServer video_server{cap, context};
  std::thread video_server_thread{
      &zmq_servers::VideoServer::start,
      video_server,
      config,
  };
  video_server_thread.join();

  return EXIT_SUCCESS;
}