from models import XRate, peewee_datetime
from config import logging, LOGGER_CONFIG

log = logging.getLogger('test_api')
fh = logging.FileHandler(LOGGER_CONFIG['file'])
fh.setLevel(LOGGER_CONFIG['level'])
fh.setFormatter(LOGGER_CONFIG['formatter'])
log.addHandler(fh)
log.setLevel(LOGGER_CONFIG['level'])


def update_xrates(from_currency, to_currency):
    log.info(f'Start update for: {from_currency}=>{to_currency}')
    xrate = XRate.select().where(XRate.from_currency == from_currency, XRate.to_currency == to_currency).first()
    log.debug(f'rate before: {xrate.rate}')
    xrate.rate += 0.01
    xrate.updated = peewee_datetime.datetime.now()
    xrate.save()
    log.debug(f'rate after: {xrate.rate}')
    log.info(f'Update finished for: {from_currency}=>{to_currency}')
    log.info('------------------')

