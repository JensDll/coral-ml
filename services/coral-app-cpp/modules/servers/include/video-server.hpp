extern "C" {
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavformat/avio.h>
#include <libavutil/imgutils.h>
#include <libswscale/swscale.h>
}
#include <opencv2/opencv.hpp>
#include <string>
#include <zmq.hpp>

#include "core.hpp"

#ifndef CORAL_APP_VIDEO_SERVER
#define CORAL_APP_VIDEO_SERVER
namespace app_servers {

class VideoServer {
 public:
  VideoServer(const app_core::Config& config, zmq::context_t& context,
              cv::VideoCapture& cap, int camIdx = 0);
  ~VideoServer();

  struct Context {
    app_core::FPSCounter fps;
  };

  using OnFrameCallback = void (*)(const cv::Mat& frame,
                                   const Context& context);

  void start(OnFrameCallback callback) const;
  void startCli(OnFrameCallback callback) const;

 private:
  cv::VideoCapture& _cap;
  zmq::context_t& _zmqContext;
  struct CapProps {
    int frameWidth;
    int frameHeight;
  } _capProps;
  struct LibavWrapper {
    SwsContext* scaler;       // Pixel layer
    AVCodecContext* encoder;  // Codec layer
    struct MuxingWrapper {
      AVFormatContext* muxer;  // Format layer
      AVIOContext* ioContext;  // Protocol layer
      AVDictionary* options;
    } muxing;
    AVFrame* outFrame;
    AVPacket* outPacket;
  } _libav;
  Context _context;
};

}  // namespace app_servers
#endif