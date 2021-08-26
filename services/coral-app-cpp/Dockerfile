FROM debian:bullseye

RUN apt update && \
    apt install -y wget unzip cmake git libtool ffmpeg \
    build-essential pkg-config libgtk-3-dev libavcodec-dev \
    libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev  \
    libtbb2 libtbb-dev libdc1394-22-dev libzmq3-dev

# Build OpenCV from source
WORKDIR /build/cv
RUN wget -q -O opencv.zip https://github.com/opencv/opencv/archive/master.zip && \
    wget -q -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/master.zip && \
    unzip -q opencv.zip && unzip -q opencv_contrib.zip

WORKDIR /build/cv/build
RUN cmake \
    -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib-master/modules \
    -D BUILD_JAVA=OFF \
    -D BUILD_FAT_JAVA_LIB=OFF \
    -D BUILD_opencv_python2=OFF \
    -D BUILD_opencv_python3=OFF \
    -D OPENCV_INSTALL_APPS_LIST="" \
    ../opencv-master
RUN cmake --build .
RUN make -j$(nproc) && make install

# Copy application code
WORKDIR /build/app
COPY . ./