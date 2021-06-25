import multiprocessing

bind = "127.0.0.1:5000"
worker_class = "gthread"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 4
