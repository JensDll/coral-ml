from flask import Flask, Response
from flask.helpers import stream_with_context
import cv2
import threading
import simplejpeg
import asyncio

app = Flask(__name__)
output_frame = None
lock = threading.Lock()


@app.route("/video")
def video_feed():
    return Response(stream_with_context(generate()), mimetype="multipart/x-mixed-replace; boundary=frame")


def read_frames(cap):
    global output_frame, lock
    print("READ")
    while True:
        has_frame, frame = cap.read()
        with lock:
            output_frame = frame.copy()


def generate():
    global output_frame, lock
    while True:
        with lock:
            if output_frame is None:
                continue

            jpg = simplejpeg.encode_jpeg(
                output_frame, quality=95, colorspace="rgb", fastdct=True)

        yield(b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
              jpg + b"\r\n")


cap = cv2.VideoCapture(0)
thread = threading.Thread(target=read_frames, args=[cap], daemon=True)
thread.start()
app.run(port=6600)
