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

  // Setup filter from RGB24 to YUV420P
  _libav.scaler = sws_getContext(_capProps.frameWidth, _capProps.frameHeight,
                                 AV_PIX_FMT_RGB24, _capProps.frameWidth,
                                 _capProps.frameHeight, AV_PIX_FMT_YUV420P,
                                 SWS_BICUBIC, NULL, NULL, NULL);

  // Setup encoder
  AVCodec* codec{ avcodec_find_encoder(AV_CODEC_ID_MPEG1VIDEO) };
  _libav.encoder = avcodec_alloc_context3(codec);
  if (!_libav.encoder) {
    std::cerr << "Could not allocate encoder\n";
  }
  _libav.encoder->bit_rate = 800'000;
  _libav.encoder->width = _capProps.frameWidth;
  _libav.encoder->height = _capProps.frameHeight;
  _libav.encoder->pix_fmt = AV_PIX_FMT_YUV420P;
  _libav.encoder->framerate = AVRational{ 30, 1 };
  _libav.encoder->time_base = AVRational{ 1, 30 };
  _libav.encoder->gop_size = 30;
  _libav.encoder->max_b_frames = 1;

  int ret{ avcodec_open2(_libav.encoder, codec, NULL) };
  if (ret < 0) {
    std::cerr << "Could not open codec for encoder\n";
  }

  // Setup output frame
  _libav.outFrame = av_frame_alloc();
  _libav.outFrame->width = _libav.encoder->width;
  _libav.outFrame->height = _libav.encoder->height;
  _libav.outFrame->format = _libav.encoder->pix_fmt;
  ret = av_image_alloc(_libav.outFrame->data, _libav.outFrame->linesize,
                       _libav.outFrame->width, _libav.outFrame->height,
                       static_cast<AVPixelFormat>(_libav.outFrame->format), 16);
  if (ret < 0) {
    std::cerr << "Could not allocate output frame\n";
  }

  // Setup output packet
  _libav.outPacket = av_packet_alloc();

  // Add video stream to muxer
  _libav.muxing.muxer = avformat_alloc_context();
  AVStream* videoStream = avformat_new_stream(_libav.muxing.muxer, NULL);
  ret = avcodec_parameters_from_context(videoStream->codecpar, _libav.encoder);
  if (ret < 0) {
    std::cerr << "Could not copy codec parameters\n";
  }
  videoStream->codecpar->codec_type = AVMEDIA_TYPE_VIDEO;

  // Setup IO context for muxer
  _libav.muxing.ioContext = nullptr;
  avio_open(&_libav.muxing.ioContext, config.publishUri.c_str(),
            AVIO_FLAG_WRITE);
  if (_libav.muxing.ioContext == NULL) {
    std::cerr << "Could not open output url\n";
  }
  _libav.muxing.muxer->pb = _libav.muxing.ioContext;

  // Miscellaneous muxer setup
  _libav.muxing.muxer->oformat = av_guess_format("mpegts", NULL, NULL);
  _libav.muxing.options = nullptr;
  av_dict_set(&_libav.muxing.options, "live", "1", 0);
  ret = avformat_write_header(_libav.muxing.muxer, &_libav.muxing.options);
  if (ret < 0) {
    std::cerr << "Could not write muxer header\n";
  }
}

app_servers::VideoServer::~VideoServer() {
  sws_freeContext(_libav.scaler);
  avcodec_free_context(&_libav.encoder);
  avformat_free_context(_libav.muxing.muxer);
  av_dict_free(&_libav.muxing.options);
  av_free(_libav.muxing.ioContext);
  av_frame_free(&_libav.outFrame);
  av_packet_free(&_libav.outPacket);
}

void app_servers::VideoServer::start(
    app_servers::OnFrameCallback callback) const {
  cv::Mat image;
  int imageLineSizes[4];
  av_image_fill_linesizes(imageLineSizes, AV_PIX_FMT_RGB24,
                          _capProps.frameWidth);
  AVStream* videoStream = _libav.muxing.muxer->streams[0];

  for (int i{ 0 };; ++i) {
    _cap.read(image);
    cv::cvtColor(image, image, cv::COLOR_BGR2RGB);
    callback(image);

    sws_scale(_libav.scaler, &image.data, imageLineSizes, 0,
              _capProps.frameHeight, _libav.outFrame->data,
              _libav.outFrame->linesize);

    _libav.outFrame->pts = i;

    int ret{ avcodec_send_frame(_libav.encoder, _libav.outFrame) };

    if (ret < 0) {
      std::cerr << "Error sending a frame for encoding\n";
      return;
    }

    while (ret >= 0) {
      ret = avcodec_receive_packet(_libav.encoder, _libav.outPacket);

      if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) {
        continue;
      } else if (ret < 0) {
        std::cerr << "Error during encoding: " << av_err2str(ret) << "\n";
        return;
      }

      // std::cout << "Encoded packet " << _libav.outPacket->pts
      //           << " (size = " << _libav.outPacket->size << ")\n";

      _libav.outPacket->stream_index = videoStream->index;
      int64_t scaled_pts =
          av_rescale_q(_libav.outPacket->pts, _libav.encoder->time_base,
                       videoStream->time_base);
      _libav.outPacket->pts = scaled_pts;

      av_write_frame(_libav.muxing.muxer, _libav.outPacket);

      av_packet_unref(_libav.outPacket);
    }
  }
}