import ffmpeg


def start_stream(frame_width, frame_height, pix_fmt, fps, publish_uri):
    process = (
        ffmpeg.input(
            "pipe:",
            format="rawvideo",
            pix_fmt=pix_fmt,
            s=f"{frame_width}x{frame_height}",
        )
        .output(
            publish_uri,
            vcodec="mpeg1video",
            framerate=fps,
            s=f"640x480",
            format="mpegts",
            video_bitrate="800k",
            segment_time="6",
            loglevel="warning",
        )
        .run_async(pipe_stdin=True)
    )

    return process
