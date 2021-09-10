#include "fps.hpp"

void app_core::FPSCounter::putFps(const cv::Mat& frame) const {
  auto currTime{ std::chrono::high_resolution_clock::now() };
  auto delta{ std::chrono::duration_cast<std::chrono::duration<double>>(
      currTime - _prevTime) };
  _prevTime = currTime;

  cv::putText(frame, std::to_string(1 / delta.count()), { 20, 20 },
              cv::FONT_HERSHEY_PLAIN, 1.0, { 0, 255, 0 });
}