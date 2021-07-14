import ffmpeg


def start_stream(size, fps, pix_fmt):
    rtmp_url = "rtmp://127.0.0.1:1935/live/coral"
    process = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt=pix_fmt, s='{}x{}'.format(*size))
        .output(rtmp_url,
                vcodec='libx264',
                pix_fmt='yuv420p',
                preset='veryfast',
                framerate=fps,
                video_bitrate='1.4M',
                maxrate='2M',
                bufsize='2M',
                segment_time='6',
                format='flv')
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )
    return process
