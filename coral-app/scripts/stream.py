import ffmpeg


def start_stream(size, fps, pix_fmt, publish_uri):
    process = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt=pix_fmt, s='{}x{}'.format(*size))
        .output(publish_uri,
                vcodec='mpeg1video',
                preset='veryfast',
                framerate=fps,
                s='{}x{}'.format(*size),
                video_bitrate='1.4M',
                maxrate='2M',
                bufsize='2M',
                segment_time='6',
                format="mpegts")
        .run_async(pipe_stdin=True)
    )
    return process
