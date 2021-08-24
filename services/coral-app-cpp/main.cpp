#include <iostream>
#include <string>
#include <unistd.h>
#include <zmq.hpp>
#include <opencv2/opencv.hpp>
#include "servers.hpp"

int main(int argc, char **argv)
{
    zmq::context_t context{1};

    cv::VideoCapture cap{};
    cap.open(0);

    if (!cap.isOpened())
    {
        return EXIT_FAILURE;
    }

    servers::VideoServer video_server{cap, context};
    video_server.start();

    return EXIT_SUCCESS;
}