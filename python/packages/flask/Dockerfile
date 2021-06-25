FROM python:3.8

WORKDIR /app

COPY /src ./

RUN apt-get update && \
    apt-get install libgl1-mesa-glx -y && \
    pip install -U pip && \
    pip install -U gunicorn flask opencv-contrib-python

ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app" ]