add_library(libav INTERFACE)

if(WIN32)
  target_link_libraries(libav INTERFACE
    -llibavcodec
    -llibavformat
    -llibavfilter
    -llibavdevice
    -llibavutil
    -llibswresample
    -llibswscale
  )
else()
  find_package(PkgConfig REQUIRED)
  pkg_check_modules(AVCODEC REQUIRED IMPORTED_TARGET libavcodec)
  pkg_check_modules(AVFORMAT REQUIRED IMPORTED_TARGET libavformat)
  pkg_check_modules(AVFILTER REQUIRED IMPORTED_TARGET libavfilter)
  pkg_check_modules(AVDEVICE REQUIRED IMPORTED_TARGET libavdevice)
  pkg_check_modules(AVUTIL REQUIRED IMPORTED_TARGET libavutil)
  pkg_check_modules(SWRESAMPLE REQUIRED IMPORTED_TARGET libswresample)
  pkg_check_modules(SWSCALE REQUIRED IMPORTED_TARGET libswscale)

  target_link_libraries(libav INTERFACE
    PkgConfig::AVCODEC
    PkgConfig::AVFORMAT
    PkgConfig::AVFILTER
    PkgConfig::AVDEVICE
    PkgConfig::AVUTIL
    PkgConfig::SWRESAMPLE
    PkgConfig::SWSCALE
  )
endif()