from flask import Flask, render_template, Response
from flask.helpers import stream_with_context
import cv2
import threading
import cv2utils

app = Flask(__name__)

output_frame = None
lock = threading.Lock()
cap = cv2.VideoCapture(0)


@app.route("/video")
def video_feed():
    return Response(stream_with_context(generate()), mimetype="multipart/x-mixed-replace; boundary=frame")


def read_frames():
    global output_frame, lock, cap
    while True:
        has_frame, frame = cap.read()
        with lock:
            if has_frame:
                output_frame = frame.copy()


def generate():
    global output_frame, lock
    while True:
        with lock:
            cv2utils.print_fps(output_frame)
            success, encoded_image = cv2.imencode(".jpg", output_frame)

            if not success:
                continue

        yield(b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
              bytearray(encoded_image) + b"\r\n")


thread = threading.Thread(target=read_frames, daemon=True)
thread.start()
