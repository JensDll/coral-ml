import zmq
import cv2
import numpy as np
import simplejpeg
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--port", "-p", default=5555, type=int)

args = parser.parse_args()

context = zmq.Context()
address = f"tcp://*:{args.port}"
socket = context.socket(zmq.PUB)
socket.bind(address)

source = cv2.VideoCapture(0)
height = source.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = source.get(cv2.CAP_PROP_FRAME_WIDTH)

print(f"Server has started. Bind to '{address}'")
print(height, width)

while True:
    frame: np.ndarray
    has_frame: bool
    has_frame, frame = source.read()

    if not has_frame:
        break

    jpg = simplejpeg.encode_jpeg(
        frame, quality=95, colorspace="bgr", fastdct=True)

    socket.send(jpg, copy=False)
