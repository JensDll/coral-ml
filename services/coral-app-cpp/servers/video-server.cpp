#include "servers.hpp"

servers::VideoServer::VideoServer(cv::VideoCapture &cap,
                                  zmq::context_t &context)
    : cap(cap), context(context) {
  cap_props.frame_width = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH));
  cap_props.frame_height = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
};

void servers::VideoServer::start() {
  std::string command{"ffmpeg"};
  // Input options
  command.append(" -f rawvideo");
  command.append(" -r 1");
  command.append(" -pix_fmt rgb24");
  command.append(" -s " + std::to_string(cap_props.frame_width) + "x" +
                 std::to_string(cap_props.frame_height));
  command.append(" -i pipe:0");  // Pipe to stdin
  // Output options
  command.append(" -f mpegts");
  command.append(" -vcodec mpeg1video");
  command.append(" -b:v 800k");
  command.append(" -s 640x480");
  command.append(" -r 30");
  command.append(" http://localhost:5060");

  std::cout << command << std::endl;

  FILE *pipeout = popen(command.c_str(), "wb");

  cv::Mat frame{};
  size_t count = cap_props.frame_width * cap_props.frame_height * 3;

  while (true) {
    cap.read(frame);

    if (frame.empty()) {
      std::cout << "Error: read empty frame" << std::endl;
      break;
    }

    cv::cvtColor(frame, frame, cv::COLOR_BGR2RGB);

    fwrite(frame.data, sizeof(uchar), count, pipeout);
  }

  fflush(pipeout);
  pclose(pipeout);
}