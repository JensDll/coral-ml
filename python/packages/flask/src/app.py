from flask import Flask, Response
from flask.helpers import stream_with_context
import cv2
import cv2utils
import threading
import numpy as np

app = Flask(__name__)

# output_frame = None
# lock = threading.Lock()
# cap = cv2.VideoCapture(0)


@app.route("/video")
def video():
    return Response(stream_with_context(generate()), mimetype="multipart/x-mixed-replace; boundary=frame")


# def read_frames():
#     global output_frame, lock
#     while True:
#         # has_frame, frame = cap.read()
#         with lock:
#             output_frame = np.zeros((500, 500, 3), dtype=np.uint8)


def generate():
    while True:
        output_frame = np.zeros((500, 500, 3), dtype=np.uint8)
        cv2utils.print_fps(output_frame)
        success, encoded_image = cv2.imencode(".jpg", output_frame)

        if not success:
            print("Could not encode image")
            continue

        yield(b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
              bytearray(encoded_image) + b"\r\n")
