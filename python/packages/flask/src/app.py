from flask import Flask, Response
from flask.helpers import stream_with_context
import cv2
from imutils.video import VideoStream
import threading
import cv2utils
import numpy as np

app = Flask(__name__)

output_frame = None
lock = threading.Lock()
vs = VideoStream(src=0).start()


@app.route("/video")
def video_feed():
    return Response(stream_with_context(generate()), mimetype="multipart/x-mixed-replace; boundary=frame")


def capture():
    global output_frame, lock
    while True:
        frame = vs.read()
        cv2utils.print_fps(output_frame)
        with lock:
            output_frame = frame.copy()


def generate():
    global output_frame, lock
    while True:
        if output_frame is None:
            continue
        with lock:
            success, encoded_image = cv2.imencode(".jpg", output_frame)
        if not success:
            continue
        yield(b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
              bytearray(encoded_image) + b"\r\n")
