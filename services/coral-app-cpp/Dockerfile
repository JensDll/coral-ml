FROM debian:bullseye AS build-env

RUN apt-get update && \
    apt-get install -y wget unzip cmake git libtool ffmpeg \
    build-essential pkg-config libgtk-3-dev libavcodec-dev \
    libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev  \
    libtbb2 libtbb-dev libdc1394-22-dev

# Build OpenCV from source
WORKDIR /build/cv
RUN wget -q -O opencv.zip https://github.com/opencv/opencv/archive/master.zip && \
    wget -q -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/master.zip && \
    unzip -q opencv.zip && unzip -q opencv_contrib.zip

WORKDIR /build/cv/build
# Options - https://docs.opencv.org/master/db/d05/tutorial_config_reference.html
RUN cmake \
    -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib-master/modules \
    -D BUILD_JAVA=OFF \
    -D BUILD_FAT_JAVA_LIB=OFF \
    -D BUILD_opencv_python2=OFF \
    -D BUILD_opencv_python3=OFF \
    -D BUILD_TESTS=OFF \
    -D BUILD_PERF_TESTS=OFF \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_opencv_apps=OFF \
    -D WITH_PROTOBUF=OFF \
    -D BUILD_PROTOBUF=OFF \
    -D OPENCV_DNN_OPENCL=OFF \
    -D WITH_GTK=OFF \
    -D WITH_WIN32UI=OFF \
    -D CMAKE_INSTALL_PREFIX=/install \
    ../opencv-master
RUN make -j$(nproc) && make install

# Build libzmq from source
WORKDIR /build/zeromq
RUN git clone --depth 1 -b v4.3.4 https://github.com/zeromq/libzmq.git && \
    cd libzmq && mkdir build
WORKDIR /build/zeromq/libzmq/build
RUN cmake ..
RUN make -j$(nproc) install
RUN DESTDIR=/install make -j$(nproc) install

# Build cppzmq from source
WORKDIR /build/zeromq
RUN git clone --depth 1 https://github.com/zeromq/cppzmq.git && \
    cd cppzmq && mkdir build
WORKDIR /build/zeromq/cppzmq/build
RUN cmake ..
RUN make -j$(nproc) install
RUN DESTDIR=/install make -j$(nproc) install

# Copy and build application code
WORKDIR /build/app
COPY . ./
WORKDIR /build/app/build
RUN cmake ..
RUN make

# Find and copy library files
# - find  https://manpages.debian.org/bullseye/findutils/find.1.en.html
# - cp    https://manpages.debian.org/bullseye/coreutils/cp.1.en.html
WORKDIR /build/lib
RUN find /install \
    -regex ".*/lib/.*\.\(so\|a\|la\).*" \
    -exec cp --no-dereference "{}" . \;

# Find and copy binary files
WORKDIR /build/bin
RUN find /install \
    -regex ".*/bin/.*" \
    -exec cp --no-dereference "{}" . \;

FROM debian:bullseye-slim AS final

RUN apt-get update && \
    apt-get install -y ffmpeg

ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/lib"
WORKDIR /app
# Copy main executable
COPY --from=build-env /build/app/build/modules/coral-app-exe/coral-app ./
# Copy libraries
COPY --from=build-env /build/lib /usr/local/lib
# Copy binaries
COPY --from=build-env /build/bin /usr/local/bin
ENTRYPOINT [ "./coral-app" ]
CMD [ "http://node-video:8080", "info" ]