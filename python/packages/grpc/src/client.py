import cv2
import grpc
import numpy as np
import argparse
from google.protobuf.empty_pb2 import Empty
from stream_pb2_grpc import StreamerStub
import stream_pb2
import cv2utils


def read_video(stub: StreamerStub):
    read_frames_req = stream_pb2.ReadFramesRequest(client_id=1)

    cam_props = stub.GetCamProps(Empty())
    res_stream = stub.ReadFrames(read_frames_req)

    win_name = "GRPC Stream"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

    try:
        for response in res_stream:
            buffer: bytes = response.frame
            frame: np.ndarray = np.frombuffer(buffer, dtype=np.uint8)
            frame = frame.reshape(cam_props.frame_height,
                                  cam_props.frame_width, 3)

            cv2utils.print_fps(frame)
            cv2.imshow(win_name, frame)

            if cv2.waitKey(1) == ord('q'):
                res_stream.cancel()
    except grpc.RpcError as e:
        print(e)
        cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description="My Script")
    parser.add_argument("--port", "-p", help="The server port",
                        type=int, default=50051)
    parser.add_argument("--host", help="The server host",
                        type=str, default="localhost")
    args = parser.parse_args()

    with grpc.insecure_channel(f'{args.host}:{args.port}') as channel:
        read_video(StreamerStub(channel))


if __name__ == '__main__':
    main()
