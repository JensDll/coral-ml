import logging
import os
import time

from modules import core


def setup_logging():
    log_id = time.strftime("log_%Y_%m_%d_%H_%M_%S")
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    fileHanlder = logging.FileHandler(filename=f"logs/{log_id}.log")
    fileHanlder.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
        handlers=[fileHanlder, streamHandler],
    )


def log_details(interpreter: core.Interpreter):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    logging.info("Model intput details ...")
    logging.info(input_details)
    logging.info("Model output details ...")
    logging.info(output_details)
