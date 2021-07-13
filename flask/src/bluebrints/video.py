from flask import Blueprint
from flask import Response, stream_with_context
import threading
import simplejpeg

bp = Blueprint('video', __name__, url_prefix='/video')

lock = threading.Lock()
output_frame = None

@bp.route("/")
def idnex():
    return Response(stream_with_context(generate()), mimetype="multipart/x-mixed-replace; boundary=frame")

def read_frames(cap):
    print("READ FRAMES")
    global output_frame, lock

    while True:
        has_frame, frame = cap.read()
        with lock:
            if has_frame:
                output_frame = frame.copy()


def generate():
    global output_frame, lock
    while True:
        with lock:
            if output_frame is None:
                continue

            jpg = simplejpeg.encode_jpeg(
                output_frame, quality=95, colorspace="rgb", fastdct=True)

        yield(b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg + b"\r\n")

print("VIDEO")
