import asyncio
import zmq
from zmq.asyncio import Context, Poller
import cv2
import simplejpeg
import argparse
import traceback
import sys
import threading
import random
import string
import aiohttp

import src.coral as coral


def pipe(context: Context):
    def id_generator(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    a = context.socket(zmq.PAIR)
    b = context.socket(zmq.PAIR)
    a.linger = b.linger = 0
    a.hwm = b.hwm = 1
    inproc = f"inproc://{id_generator(16)}"
    a.bind(inproc)
    b.connect(inproc)
    return a, b


async def publisher(context: Context, peer: zmq.Socket, camera_source, args: argparse.Namespace):
    address = f"tcp://*:{args.pub_port}"
    publisher = context.socket(zmq.PUB)
    publisher.bind(address)
    print(f"(PUB) Bind to '{address}'")

    poller = Poller()
    poller.register(peer, zmq.POLLIN)
    poller.register(publisher, zmq.POLLOUT)

    while True:
        try:
            items = dict(await poller.poll())
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

            await publisher.send(jpg, copy=False)

    publisher.close()
    peer.close()


async def model_manager(context: Context, kill: zmq.Socket, args: argparse.Namespace):
    address = f"tcp://*:{args.rep_port}"
    reply = context.socket(zmq.REP)
    reply.bind(address)
    print(f"(REP) Bind to '{address}'")

    coral.set_base_uri(args.api)
    session = aiohttp.ClientSession()

    while True:
        id = await reply.recv_string()

        await coral.load_model(session, id)

        await reply.send_string("OK")

    await session.close()


async def test():
    coral.set_base_uri("http://localhost:5000/api")
    session = aiohttp.ClientSession()
    await coral.load_model(session, 9)
    await session.close()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pub_port", default=5500, type=int)
    parser.add_argument("--rep_port", default=5600, type=int)
    parser.add_argument("--api", default="http://localhost:5000/api", type=str)
    args = parser.parse_args()

    context = Context()
    camera_source = cv2.VideoCapture(0)

    kill, peer = pipe(context)

    model_manager_thread = threading.Thread(
        target=asyncio.run,
        args=[
            model_manager(
                context=context,
                kill=kill,
                args=args
            )
        ])
    model_manager_thread.daemon = True
    model_manager_thread.start()

    try:
        await publisher(
            context=context,
            peer=peer,
            camera_source=camera_source,
            args=args
        )
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
    asyncio.run(main())
