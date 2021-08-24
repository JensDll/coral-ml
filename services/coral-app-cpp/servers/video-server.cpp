#include "servers.hpp"

servers::VideoServer::VideoServer(cv::VideoCapture &cap, zmq::context_t &context)
    : cap(cap), context(context){};

void servers::VideoServer::start()
{
    cv::Mat frame{};

    while (true)
    {
        cap.read(frame);

        if (frame.empty())
        {
            std::cout << "Error: read empty frame" << std::endl;
        }

        cv::imshow("Stream", frame);

        if (cv::waitKey(1) >= 0)
        {
            break;
        }
    }
}