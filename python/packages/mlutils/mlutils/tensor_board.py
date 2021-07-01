import os
import pathlib


def get_run_logdir():
    import time
    root_log_dir = pathlib.Path()
    parts = pathlib.Path().resolve().parts
    root_log_dir = parts[:parts.index("python") + 1]
    root_log_dir = pathlib.Path(*root_log_dir).joinpath("my_logs")
    run_id = time.strftime("run_%Y_%m_%d_%H_%M_%S")
    return root_log_dir.joinpath(run_id)
