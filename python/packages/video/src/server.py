import zmq
import cv2
import numpy as np
import simplejpeg
import argparse
import traceback
import sys
from inference import detection

parser = argparse.ArgumentParser()
parser.add_argument("--pub_port", default=5555, type=int)
parser.add_argument("--rep_port", default=5556, type=int)

args = parser.parse_args()


class Publisher:
    def __init__(self) -> None:
        self.context = zmq.Context()
        self.source = cv2.VideoCapture(0)

    def publish(self):
        address = f"tcp://*:{args.pub_port}"
        pub = self.context.socket(zmq.PUB)
        pub.bind(address)
        print(f"Bind to '{address}' (PUB)")

        while True:
            has_frame, frame = self.source.read()

            if not has_frame:
                break

            frame = detection.run_inference(frame)

            jpg = simplejpeg.encode_jpeg(
                frame, quality=95, colorspace="bgr", fastdct=True)
            pub.send(jpg, copy=False)


def main():
    pub = Publisher()

    try:
        pub.publish()
    except (KeyboardInterrupt, SystemExit):
        print('Exit due to keyboard interrupt')
    except Exception as ex:
        print('Python error with no Exception handler')
        print('Traceback error:', ex)
        traceback.print_exc()
    finally:
        pub.source.release()
        sys.exit()


if __name__ == "__main__":
    main()
