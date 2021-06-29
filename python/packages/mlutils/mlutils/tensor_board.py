import os
import pathlib


def get_run_logdir():
    import time
    root_log_dir = pathlib.Path()
    parts = pathlib.Path().resolve().parts
    root_log_dir = parts[:parts.index("python") + 1]
    root_log_dir = pathlib.Path(*root_log_dir).joinpath("my_logs")
    run_id = time.strftime("run__%Y_%m_%s_%H-%M-%S")
    return root_log_dir.joinpath(run_id)


print(get_run_logdir())
