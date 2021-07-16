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
            preset="veryfast",
            framerate=fps,
            video_bitrate="1.4M",
            maxrate="2M",
            bufsize="2M",
            segment_time="6",
            format="mpegts",
        )
        .run_async(pipe_stdin=True)
    )
    return process
