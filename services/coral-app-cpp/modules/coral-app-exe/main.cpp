#include "main.hpp"

#include <iostream>
#include <opencv2/opencv.hpp>
#include <string>
#include <thread>
#include <zmq.hpp>

#include "video-server.hpp"

// int main(int argc, char** argv) {
//   if (argc != 3) {
//     std::cout << "Invalid number of arguments " << argc << std::endl;
//     return EXIT_FAILURE;
//   }

//   coral_app_main::Config config;
//   config.publish_uri = std::string{ argv[1] };
//   config.loglevel = std::string{ argv[2] };

//   zmq::context_t context{ 1 };

//   cv::VideoCapture cap;
//   cap.open(0);

//   if (!cap.isOpened()) {
//     return EXIT_FAILURE;
//   }

//   zmq_servers::VideoServer video_server{ cap, context };
//   std::thread video_server_thread{
//     zmq_servers::VideoServer::start,
//     std::ref(video_server),
//     std::ref(config),
//   };
//   video_server_thread.join();

//   return EXIT_SUCCESS;
// }

// void cvmat_to_avframe(cv::Mat* mat) {
//   AVFrame dst;
//   cv::Size size = mat->size();
//   AVCodec* encoder = avcodec_find_encoder(AV_CODEC_ID_MPEG1VIDEO);
//   AVFormatContext* outContainer = avformat_alloc_context();
//   AVStream* outStream = avformat_new_stream(outContainer, encoder);

//   outStream->codec->pix_fmt = AV_PIX_FMT_YUV420P;
//   outStream->codec->width = frame->cols;
//   outStream->codec->height = frame->rows;
//   avpicture_fill((AVPicture*)&dst, frame->data, PIX_FMT_BGR24,
//                  outStream->codec->width, outStream->codec->height);
//   dst.width = frameSize.width;
//   dst.height = frameSize.height;
//   SaveFrame(&dst, dst.width, dst.height, 0);
//   return dst;
// }

#include <libavcodec/avcodec.h>
#include <libavutil/imgutils.h>
#include <libavutil/opt.h>

static void encode(AVCodecContext* enc_ctx, AVFrame* frame, AVPacket* pkt,
                   FILE* outfile) {
  int ret;

  if (frame) printf("Send frame %3" PRId64 "\n", frame->pts);

  ret = avcodec_send_frame(enc_ctx, frame);
  if (ret < 0) {
    fprintf(stderr, "Error sending a frame for encoding\n");
    exit(1);
  }

  while (ret >= 0) {
    ret = avcodec_receive_packet(enc_ctx, pkt);
    if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF)
      return;
    else if (ret < 0) {
      fprintf(stderr, "Error during encoding\n");
      exit(1);
    }

    printf("Write packet %3" PRId64 " (size=%5d)\n", pkt->pts, pkt->size);
    fwrite(pkt->data, 1, pkt->size, outfile);
    av_packet_unref(pkt);
  }
}

void cvmat_to_avframe(const cv::Mat& mat) {
  cv::Size size = mat.size();

  AVCodec* codec = avcodec_find_encoder(AV_CODEC_ID_MPEG1VIDEO);
  AVCodecContext* c = avcodec_alloc_context3(codec);
  AVPacket* pkt = av_packet_alloc();
  uint8_t endcode[] = { 0, 0, 1, 0xb7 };

  c->width = size.width;
  c->height = size.height;
  c->pix_fmt = AV_PIX_FMT_RGB24;

  int ret = avcodec_open2(c, codec, NULL);

  AVFrame* result = av_frame_alloc();
  result->width = c->width;
  result->height = c->height;
  result->format = c->pix_fmt;

  ret = av_frame_get_buffer(result, 0);

  FILE* f = fopen("test", "wb");

  /* encode 1 second of video */
  for (int i{ 0 }; i < 25; i++) {
    fflush(stdout);
    /* make sure the frame data is writable */
    ret = av_frame_make_writable(result);
    if (ret < 0) exit(1);
    /* prepare a dummy image */
    /* Y */
    for (int y{ 0 }; y < c->height; y++) {
      for (int x{ 0 }; x < c->width; x++) {
        result->data[0][y * result->linesize[0] + x] = x + y + i * 3;
      }
    }
    /* Cb and Cr */
    for (int y{ 0 }; y < c->height / 2; y++) {
      for (int x{ 0 }; x < c->width / 2; x++) {
        result->data[1][y * result->linesize[1] + x] = 128 + y + i * 2;
        result->data[2][y * result->linesize[2] + x] = 64 + x + i * 5;
      }
    }
    result->pts = i;
    /* encode the image */
    encode(c, result, pkt, f);
  }

  /* flush the encoder */
  encode(c, NULL, pkt, f);
  /* add sequence end code to have a real MPEG file */
  fwrite(endcode, 1, sizeof(endcode), f);

  fclose(f);

  avcodec_free_context(&c);
  av_frame_free(&result);
  av_packet_free(&pkt);
}

int main() {
  cv::Mat mat{ cv::Mat::zeros(480, 640, CV_8UC3) };
  cvmat_to_avframe(mat);
}
