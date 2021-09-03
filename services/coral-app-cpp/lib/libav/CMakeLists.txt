# find_package(PkgConfig REQUIRED)
# pkg_check_modules(AVCODEC     REQUIRED IMPORTED_TARGET libavcodec)
# pkg_check_modules(AVFORMAT    REQUIRED IMPORTED_TARGET libavformat)
# pkg_check_modules(AVFILTER    REQUIRED IMPORTED_TARGET libavfilter)
# pkg_check_modules(AVDEVICE    REQUIRED IMPORTED_TARGET libavdevice)
# pkg_check_modules(AVUTIL      REQUIRED IMPORTED_TARGET libavutil)
# pkg_check_modules(SWRESAMPLE  REQUIRED IMPORTED_TARGET libswresample)
# pkg_check_modules(SWSCALE     REQUIRED IMPORTED_TARGET libswscale)

# add_library(ffmpeg INTERFACE)

# target_link_libraries(ffmpeg INTERFACE
#   PkgConfig::AVCODEC
#   PkgConfig::AVFORMAT
#   PkgConfig::AVFILTER
#   PkgConfig::AVDEVICE
#   PkgConfig::AVUTIL
#   PkgConfig::SWRESAMPLE
#   PkgConfig::SWSCALE
# )

add_library(libav INTERFACE)

find_package(LIBAV REQUIRED)

if(LIBAV_FOUND)
  message("Found FFMPEG/LibAV libraries")
  include_directories(${LIBAV_INCLUDE_DIR})
  target_link_libraries(libav ${LIBAV_LIBRARIES})
else()
  message("Can't find libavcodec, libavformat or libavutil. Add them!")
endif()