import grpc
import cv2
import numpy as np
from concurrent import futures
import imutils
import argparse
import threading
import socket
import os

import image_pb2
from image_pb2_grpc import ImageClassifierServicer, add_ImageClassifierServicer_to_server


class ImageClassifier(ImageClassifierServicer):
    def LoadModel(self, request, context):
        pass


def start_server(args: argparse.Namespace):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streamer = ImageClassifier()
    add_ImageClassifierServicer_to_server(streamer, server)
    address = f"[::]:{args.port}"
    server.add_insecure_port(address)
    print(f"Server listening at '{address}'")
    server.start()
    return server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", help="The server port.",
                        type=int, default=5050)
    args = parser.parse_args()

    try:
        server = start_server(args)
        server.wait_for_termination()
    except (KeyboardInterrupt, SystemExit):
        print('Exit due to keyboard interrupt')
    except Exception as ex:
        print('Python error with no Exception handler')
        print('Traceback error:', ex)


if __name__ == '__main__':
    main()
