#include <zmq.hpp>
#include <opencv2/opencv.hpp>

namespace servers
{
    class VideoServer
    {
        cv::VideoCapture &cap;
        zmq::context_t &context;

    public:
        VideoServer(cv::VideoCapture &cap, zmq::context_t &context);
        void start();
    };
}
