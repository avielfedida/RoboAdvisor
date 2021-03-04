from datetime import datetime
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from uuid import uuid4
from colorlog import ColoredFormatter
import os   

# From the following links:
# https://stackoverflow.com/questions/28180159/how-do-i-can-format-exception-stacktraces-in-python-logging
# https://www.toptal.com/python/in-depth-python-logging
# https://stackoverflow.com/questions/1278705/when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number

LOG_FORMAT = '%(asctime)s|%(levelname)s|%(message)s|'
LOG_COLORED_FORMAT = '%(cyan)s[%(asctime)s]%(reset)s%(yellow)s[%(levelname)s]%(reset)s%(red)s[%(message)s]'
DT_FORMAT = '%m/%d/%Y %I:%M:%S %p'
LOG_DIR = "./logs"


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        s = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter(LOG_COLORED_FORMAT, DT_FORMAT))
    return console_handler


def get_file_handler():
    logfilepath = os.path.join(LOG_DIR, f"Logfile-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log")#-{uuid4()}.log")
    # file_handler = TimedRotatingFileHandler(logfilepath, when='midnight')
    file_handler = logging.FileHandler(logfilepath)
    file_handler.setFormatter(OneLineExceptionFormatter(LOG_FORMAT, DT_FORMAT))
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough

    # Console handler
    logger.addHandler(get_console_handler())

    # File handler
    logger.addHandler(get_file_handler())

    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False

    return logger
