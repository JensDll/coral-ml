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
            preset="ultrafast",
            framerate=fps,
            s=f"{int(frame_width * 0.8)}x{int(frame_height * 0.8)}",
            format="mpegts",
            video_bitrate="800k",
            maxrate="1M",
            bufsize="1M",
            segment_time="6",
            loglevel="quiet",
        )
        .run_async(pipe_stdin=True)
    )
    return process
