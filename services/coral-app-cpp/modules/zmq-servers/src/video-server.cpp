#include "video-server.hpp"

#include "main.hpp"

zmq_servers::VideoServer::VideoServer(cv::VideoCapture& cap,
                                      zmq::context_t& context)
    : m_cap{ cap },
      m_context{ context },
      m_cap_props{ static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH)),
                   static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT)) } {}

std::string zmq_servers::VideoServer::build_ffmpeg_command(
    const coral_app_main::Config& config) const {
  std::string command{ "ffmpeg" };
  // Input options
  command.append(" -f rawvideo");
  command.append(" -r 1");
  command.append(" -pix_fmt rgb24");
  command.append(" -s " + std::to_string(m_cap_props.frame_width) + "x" +
                 std::to_string(m_cap_props.frame_height));
  command.append(" -i pipe:0");  // Pipe to stdin
  // Output options
  command.append(" -f mpegts");
  command.append(" -vcodec mpeg1video");
  command.append(" -b:v 800k");
  command.append(" -s 640x480");
  command.append(" -r 30");
  command.append(" -loglevel " + config.loglevel);
  command.append(" " + config.publish_uri);

  return command;
}

void zmq_servers::VideoServer::start(
    const coral_app_main::Config& config) const {
  std::string command = build_ffmpeg_command(config);

  std::cout << command << std::endl;

  FILE* pipeout = popen(command.c_str(), "wb");

  if (!pipeout) {
    throw std::runtime_error("popen failes");
  }

  cv::Mat frame;
  size_t count = m_cap_props.frame_width * m_cap_props.frame_height * 3;

  while (true) {
    bool success = m_cap.read(frame);

    if (!success) {
      std::cout << "Error reading frame" << std::endl;
      break;
    }

    cv::cvtColor(frame, frame, cv::COLOR_BGR2RGB);

    fwrite(frame.data, sizeof(uchar), count, pipeout);
  }

  fflush(pipeout);
  pclose(pipeout);
}