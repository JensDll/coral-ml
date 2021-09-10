#include <chrono>
#include <opencv2/opencv.hpp>
#include <sstream>

#ifndef CORAL_APP_FPS
#define CORAL_APP_FPS
namespace app_core {

class FPSCounter {
 public:
  void putFps(const cv::Mat& frame) const;

 private:
  mutable std::chrono::high_resolution_clock::time_point _prevTime{
    std::chrono::high_resolution_clock::now()
  };
};

}  // namespace app_core
#endif