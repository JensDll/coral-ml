from google.protobuf import message
import grpc
import cv2
import numpy as np
from concurrent import futures
import imutils
import argparse
import threading

import stream_pb2
from stream_pb2_grpc import StreamerServicer, add_StreamerServicer_to_server


class Streamer(StreamerServicer):
    def __init__(self, camera_idx: int) -> None:
        cap = cv2.VideoCapture(camera_idx)
        frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.camera_idx = camera_idx
        self.frame_width = int(frame_width)
        self.frame_height = int(frame_height)
        self.cap = cap

    def GetCamProps(self, request, context):
        return stream_pb2.CamProps(frame_width=self.frame_width,
                                   frame_height=self.frame_height)

    def ReadFrames(self, request, context):
        print(f"Server called by client ({request.client_id})")
        print("--------------")

        stop_event = threading.Event()

        def on_rpc_done():
            stop_event.set()
            print(f"Stop client ({request.client_id})")

        context.add_callback(on_rpc_done)

        def response_messages():
            while context.is_active():
                has_frame, frame = self.cap.read()
                if not has_frame:
                    break
                yield stream_pb2.Frame(frame=frame.tobytes())

        return response_messages()


def start_server(port: int, camera_idx: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streamer = Streamer(camera_idx)
    add_StreamerServicer_to_server(streamer, server)
    address = f"[::]:{port}"
    server.add_insecure_port(address)
    print(f"Server listening at '{address}'")
    server.start()
    return server, streamer


def main():
    parser = argparse.ArgumentParser(description="My Script")
    parser.add_argument("--port", "-p", help="The server port.",
                        type=int, default=50051)
    parser.add_argument('--camera_idx', "-i", help='Index of which video source to use.',
                        type=int, default=0)
    args = parser.parse_args()
    server, streamer = start_server(args.port, args.camera_idx)
    server.wait_for_termination()
    streamer.cap.release()


if __name__ == '__main__':
    main()
