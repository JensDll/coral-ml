import grpc
import cv2
import numpy as np
from concurrent import futures
import imutils
import argparse
import threading
import socket
import os

import stream_pb2
from stream_pb2_grpc import StreamerServicer, add_StreamerServicer_to_server


class Streamer(StreamerServicer):
    def __init__(self, args: argparse.Namespace) -> None:
        self.cap = cv2.VideoCapture(args.camera_idx)
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def GetCamProps(self, request, context):
        return stream_pb2.CamProps(frame_width=self.frame_width, frame_height=self.frame_height)

    def ReadFrames(self, request, context):
        print(f"Server called by client ({request.client_id})")
        print("--------------")

        stop_event = threading.Event()

        def on_rpc_done():
            stop_event.set()
            print(f"Stopping client ({request.client_id})")

        context.add_callback(on_rpc_done)

        def response_messages():
            while context.is_active():
                has_frame, img_bgr = self.cap.read()
                if not has_frame:
                    break
                img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
                img_bytes = img_rgb.tobytes()
                yield stream_pb2.Frame(frame=img_bytes)

        return response_messages()


def start_server(args: argparse.Namespace):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streamer = Streamer(args)
    add_StreamerServicer_to_server(streamer, server)
    address = f"[::]:{args.port}"
    server.add_insecure_port(address)
    print(f"Server listening at '{address}'")
    server.start()
    return server, streamer


def main():
    default_model_dir = './all_models'
    default_model = 'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite'
    default_labels = 'coco_labels.txt'

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", help="The server port.",
                        type=int, default=50051)
    parser.add_argument('--camera_idx', "-i", help='Index of which video source to use.',
                        type=int, default=0)
    parser.add_argument('--model', help='.tflite model path',
                        default=os.path.join(default_model_dir, default_model))
    parser.add_argument('--labels', help='label file path',
                        default=os.path.join(default_model_dir, default_labels))
    args = parser.parse_args()

    server, streamer = start_server(args)
    server.wait_for_termination()
    streamer.cap.release()


if __name__ == '__main__':
    main()
