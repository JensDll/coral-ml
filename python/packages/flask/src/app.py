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
# video_stream = None VideoStream(src=0).start()


@app.route("/video")
def video_feed():
    return Response(stream_with_context(generate()), mimetype="multipart/x-mixed-replace; boundary=frame")


def read_frames():
    global output_frame, lock
    while True:
        # frame = video_stream.read()
        with lock:
            # if frame is not None:
            output_frame = np.zeros((500, 500, 3), dtype=np.uint8)


def generate():
    global output_frame, lock
    while True:
        with lock:
            if output_frame is None:
                continue

            cv2utils.print_fps(output_frame)
            success, encoded_image = cv2.imencode(".jpg", output_frame)

            if not success:
                continue

        yield(b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
              bytearray(encoded_image) + b"\r\n")


thread = threading.Thread(target=read_frames, daemon=True)
thread.start()
