import logging
from logging.handlers import RotatingFileHandler
from functools import wraps

from hacktribe_editor.ht_editor_config import open_config

ht_log_level = getattr(logging, open_config()['log']['level'].upper())

ht_log_format = '%(asctime)s, %(levelname)-8s [%(filename)s:%(module)s:%(funcName)s:%(lineno)d] %(message)s'

formatter = logging.Formatter(ht_log_format)

log = logging.getLogger()
log.setLevel(logging.DEBUG)

console_log = logging.StreamHandler()
console_log.setLevel(ht_log_level)
console_log.setFormatter(formatter)
log.addHandler(console_log)

file_log = RotatingFileHandler(
    'ht_editor.log',
    'w',
    maxBytes=1073741824,
    backupCount=3,
)
file_log.doRollover()
file_log.setLevel(logging.DEBUG)
file_log.setFormatter(formatter)
log.addHandler(file_log)


def set_log_level(level):
    log.info('Called set_log_level: level=%s', level)
    level = getattr(logging, level.upper())
    for handler in log.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setLevel(level)
            break


def log_debug(func):

    @wraps(func)
    def debug_log(*args, **kwargs):
        saved_args = locals()

        msg = str(saved_args['func']) + ' args: ' + str(
            saved_args['args']) + ' kwargs: ' + str(saved_args['kwargs'])

        try:
            if log.getEffectiveLevel() <= logging.DEBUG:
                log.debug(msg)
            return func(*args, **kwargs)
        except:
            logging.error("Exception. %s", msg)
            raise

    return debug_log
