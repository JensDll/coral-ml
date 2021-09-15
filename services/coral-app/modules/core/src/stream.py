import logging
import traceback
import time

import ffmpeg

from modules import core


def start_stream(cap_props: core.types.CapProps):
    stream = ffmpeg.input(
        "pipe:",
        format="rawvideo",
        pix_fmt="rgb24",
        s=f"{cap_props['frameWidth']}x{cap_props['frameHeight']}",
    )
    stream = ffmpeg.output(
        stream,
        core.Config.Uri.PUBLISH_VIDEO,
        vcodec="mpeg1video",
        framerate=cap_props["fps"],
        s=f"640x480",
        format="mpegts",
        video_bitrate="800k",
        loglevel=core.Config.FFmpeg.LOGLEVEL,
    )
    stream = ffmpeg.run_async(stream, pipe_stdin=True)
    return stream


def restart_stream(cap_props: core.types.CapProps, intervall: int = 4):
    logging.error("FFMPEG Error")
    logging.error(traceback.format_exc())
    while True:
        time.sleep(intervall)
        logging.info("Restarting Stream")
        try:
            yield start_stream(cap_props)
            break
        except Exception:
            pass
