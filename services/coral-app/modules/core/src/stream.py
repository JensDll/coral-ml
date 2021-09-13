from modules.core.src.config import CONFIG
import ffmpeg
import logging
import traceback
import time
from modules import core


def start_stream(cap_props: core.typedef.CapProps):
    process = (
        ffmpeg.input(
            "pipe:",
            format="rawvideo",
            pix_fmt="rgb24",
            s=f"{cap_props['frameWidth']}x{cap_props['frameHeight']}",
        )
        .output(
            core.CONFIG.URI.PUBLISH_VIDEO,
            vcodec="mpeg1video",
            framerate=cap_props["fps"],
            s=f"640x480",
            format="mpegts",
            video_bitrate="800k",
            loglevel=CONFIG.FFMPEG.LOGLEVEL,
        )
        .run_async(pipe_stdin=True)
    )

    return process


def restart_stream(cap_props: core.typedef.CapProps, intervall: int = 4):
    logging.error("FFMPEG Error")
    logging.error(traceback.format_exc())
    while True:
        time.sleep(intervall)
        logging.info("Restarting Stream")
        try:
            yield start_stream(cap_props)
            break
        except:
            pass
