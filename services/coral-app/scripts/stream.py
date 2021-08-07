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
            s=f"{frame_width}x{frame_height}",
            format="mpegts",
            video_bitrate="400k",
            maxrate="600k",
            bufsize="600k",
            segment_time="6",
        )
        .run_async(pipe_stdin=True)
    )

    return process
