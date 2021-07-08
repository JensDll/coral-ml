from modelRepository import ModelRepository
import zmq
import cv2
import simplejpeg
import argparse
import traceback
import sys
import aiohttp
import asyncio


async def publish(context: zmq.Context, session: aiohttp.ClientSession, camera_source, args: argparse.Namespace):
    address = f"tcp://*:{args.pub_port}"
    publisher = context.socket(zmq.PUB)
    publisher.bind(address)
    print(f"(PUB) Bind to '{address}'")

    address = f"tcp://*:{args.pull_port}"
    puller = context.socket(zmq.PULL)
    puller.bind(address)
    print(f"(PULL) Bind to '{address}'")

    poller = zmq.Poller()
    poller.register(puller, zmq.POLLIN)
    poller.register(publisher, zmq.POLLOUT)

    model_repo = ModelRepository(args.api, session)

    while True:
        try:
            items = dict(poller.poll())
        except:
            break

        if puller in items:
            id = puller.recv()
            print(f"PULL {id}")
            await model_repo.get_by_id(id.decode("utf-8"))

        if publisher in items:
            has_frame, frame = camera_source.read()

            if not has_frame:
                break

            jpg = simplejpeg.encode_jpeg(
                frame, quality=95, colorspace="bgr", fastdct=True)

            publisher.send(jpg, copy=False)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pub_port", default=5555, type=int)
    parser.add_argument("--pull_port", default=5556, type=int)
    parser.add_argument(
        "--api", help="The address of the TFLite API server", type=str)

    args = parser.parse_args()

    context = zmq.Context()
    session = aiohttp.ClientSession()
    camera_source = cv2.VideoCapture(0)

    try:
        await publish(context, session, camera_source, args)
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
