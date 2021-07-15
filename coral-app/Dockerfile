FROM debian:buster

# add Google repository and common packages
RUN apt-get update && apt-get install -y curl gnupg udev wget && \
    echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | \
    tee /etc/apt/sources.list.d/coral-edgetpu.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    # https://coral.ai/docs/m2/get-started/#2-install-the-pcie-driver-and-edge-tpu-runtime
    apt-get install -y libedgetpu1-std && apt-get clean

WORKDIR /app

# copy entrypoint and requirements
COPY requirements.txt main.py ./

# install python and the tflite runtime
RUN apt-get install -y python3 python3-pip python3-tflite-runtime \
    # https://github.com/conda-forge/pygridgen-feedstock/issues/10#issuecomment-365914605
    libgl1-mesa-glx

# update pip
RUN python3 -m pip install -U pip
# install requirements
RUN python3 -m pip install -r requirements.txt && \
    apt-get clean

COPY /src ./src
COPY /scripts ./scripts

EXPOSE 7100 7200

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
