import logging
import os


def build_logger(name, log_file="data.log"):

    if not os.path.exists(log_file):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # 创建一个logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # 设置日志级别

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)

    # 创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
