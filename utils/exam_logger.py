import logging
import os


import logging
from logging.handlers import RotatingFileHandler

loggers = {}


def setup_logging(logger_name="example_logger", log_file="app.log", level=logging.INFO):
    if logger_name in loggers:
        return loggers[logger_name]

    if not os.path.exists(log_file):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # 创建一个日志记录器
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # 创建一个处理器，并设置级别和格式
    handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
    handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # 添加文件处理器到日志记录器
    logger.addHandler(handler)

    # 添加一个流处理器，用于输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)  # 只输出error以上级别的日志到控制台
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 避免重复添加处理器
    logger.propagate = False

    # 缓存创建好的日志记录器
    loggers[logger_name] = logger

    return logger


# 获取日志记录器的函数
def get_logger(logger_name, log_file):
    return loggers.get(logger_name, setup_logging(logger_name, log_file))
