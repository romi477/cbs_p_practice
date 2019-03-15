import logging

DB_NAME = 'currency_snake.db'

LOGGER_CONFIG = {
    'level': logging.DEBUG,
    'file': 'logfile.log',
    'formatter': logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s: %(message)s')
}

HTTP_TIMEOUT = 20