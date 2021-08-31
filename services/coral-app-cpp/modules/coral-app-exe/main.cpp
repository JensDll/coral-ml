#include "main.hpp"

#include <iostream>
#include <opencv2/opencv.hpp>
#include <string>
#include <thread>
#include <zmq.hpp>

#include "zmq-servers.hpp"

int main(int argc, char **argv) {
  if (argc != 3) {
    std::cout << "Invalid number of arguments " << argc << std::endl;
    return EXIT_FAILURE;
  }

  coral_app_main::Config config{};
  config.publish_uri = std::string{argv[1]};
  config.loglevel = std::string{argv[2]};

  // std::string command{"ffmpeg"};
  // // Input options
  // command.append(" -f rawvideo");
  // command.append(" -r 1");
  // command.append(" -pix_fmt rgb24");
  // command.append(" -s 640x480");
  // command.append(" -i pipe:0");  // Pipe to stdin
  // // Output options
  // command.append(" -f mpegts");
  // command.append(" -vcodec mpeg1video");
  // command.append(" -b:v 800k");
  // command.append(" -s 640x480");
  // command.append(" -r 30");
  // command.append(" -loglevel " + config.loglevel);
  // command.append(" " + config.publish_uri);

  // std::cout << command << std::endl;

  // size_t count = 480 * 640 * 3;
  // cv::Mat m{480, 640, CV_8UC3, cv::Scalar{0, 0, 0}};

  // FILE *pipeout = popen(command.c_str(), "wb");

  // if (!pipeout) {
  //   throw std::runtime_error("popen failed");
  // }

  // fwrite(m.data, sizeof(uchar), count, pipeout);

  // fflush(pipeout);
  // pclose(pipeout);

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