FROM python:3.9.7-bullseye

# Add Google repository and install required packages
RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | \
    tee /etc/apt/sources.list.d/coral-edgetpu.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    # https://github.com/conda-forge/pygridgen-feedstock/issues/10#issuecomment-365914605
    apt-get install -y libedgetpu1-std python3-tflite-runtime libgl1-mesa-glx ffmpeg

# Switch to app directory
WORKDIR /app

# Copy entrypoint and requirements
COPY requirements.txt main.py ./

# Install requirements
RUN pip install --upgrade --requirement requirements/prod.txt

# Copy the rest
COPY /src ./src
COPY /scripts ./scripts

# Include python3-tflite-runtime location in python path
ENV PYTHONPATH="/usr/lib/python3:/usr/lib/python3/dist-packages"

# Do not load variables from development .env file
ENV MODE=PROD

# Port settings
ENV CORAL_PORT_MODEL_MANAGER=7000
ENV CORAL_PORT_IMAGE_CLASSIFICATION=7020
ENV CORAL_PORT_IMAGE_SETTINGS=7021
ENV CORAL_PORT_VIDEO_SETTINGS=7041

# External resources
ENV RECORD_API_URI=http://proxy/record-api
ENV NODE_API_URI=http://node-video:8080

ENTRYPOINT [ "python", "main.py" ]
