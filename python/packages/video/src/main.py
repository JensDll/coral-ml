import zmq
import cv2
import simplejpeg
import argparse
import traceback
import sys
import threading
import random
import string


def id_generator(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def pipe(context: zmq.Context):
    a = context.socket(zmq.PAIR)
    b = context.socket(zmq.PAIR)
    a.linger = b.linger = 0
    a.hwm = b.hwm = 1
    inproc = f"inproc://{id_generator(16)}"
    a.bind(inproc)
    b.connect(inproc)
    return a, b


def publisher(context: zmq.Context, peer: zmq.Socket, camera_source, args: argparse.Namespace):
    global stop_event

    address = f"tcp://*:{args.pub_port}"
    publisher = context.socket(zmq.PUB)
    publisher.bind(address)
    print(f"(PUB) Bind to '{address}'")

    poller = zmq.Poller()
    poller.register(peer, zmq.POLLIN)
    poller.register(publisher, zmq.POLLOUT)

    while True:
        try:
            items = dict(poller.poll())
        except:
            break

        if peer in items:
            print("KILL")

        if publisher in items:
            has_frame, frame = camera_source.read()

            if not has_frame:
                break

            jpg = simplejpeg.encode_jpeg(
                frame, quality=95, colorspace="bgr", fastdct=True)

            publisher.send(jpg, copy=False)

    publisher.close()
    peer.close()


def model_manager(context: zmq.Context, kill: zmq.Socket, args: argparse.Namespace):
    global stop_event

    address = f"tcp://*:{args.rep_port}"
    receiver = context.socket(zmq.REP)
    receiver.bind(address)
    print(f"(REP) Bind to '{address}'")

    while True:
        msg = receiver.recv()
        print(msg)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pub_port", default=5500, type=int)
    parser.add_argument("--rep_port", default=5600, type=int)

    args = parser.parse_args()

    context = zmq.Context()
    camera_source = cv2.VideoCapture(0)

    kill, peer = pipe(context)

    model_manager_thread = threading.Thread(
        target=model_manager, args=[context, kill, args])
    model_manager_thread.daemon = True
    model_manager_thread.start()

    try:
        publisher(context, peer, camera_source, args)
    except (KeyboardInterrupt, SystemExit):
        print('Exit due to keyboard interrupt')
    except Exception as ex:
        print('Python error with no Exception handler')
        print('Traceback error:', ex)
        traceback.print_exc()
    finally:
        camera_source.release()
        sys.exit()


if __name__ == "__main__":
    main()
