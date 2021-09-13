FROM python:3.9.7-bullseye

# Add Google repository and install required packages
RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | \
    tee /etc/apt/sources.list.d/coral-edgetpu.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    # https://github.com/conda-forge/pygridgen-feedstock/issues/10#issuecomment-365914605
    apt-get install -y libedgetpu1-std python3-tflite-runtime libgl1-mesa-glx ffmpeg

# Include python3-tflite-runtime location in python path
ENV PYTHONPATH="/usr/lib/python3:/usr/lib/python3/dist-packages"

# Switch to app directory
WORKDIR /app

# Copy entrypoint and requirements
COPY requirements.txt main.py ./

# Install requirements
RUN pip install --upgrade --requirement requirements/prod.txt

# Copy the rest
COPY /src ./src
COPY /scripts ./scripts

ENTRYPOINT [ "python", "main.py" ]
