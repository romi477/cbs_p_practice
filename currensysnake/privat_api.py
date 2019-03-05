from models import XRate, peewee_datetime
from config import logging, LOGGER_CONFIG
import requests

log = logging.getLogger('privat_api')
fh = logging.FileHandler(LOGGER_CONFIG['file'])
fh.setLevel(LOGGER_CONFIG['level'])
fh.setFormatter(LOGGER_CONFIG['formatter'])
log.addHandler(fh)
log.setLevel(LOGGER_CONFIG['level'])

url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'

def update_xrates(from_currency, to_currency):
    log.info(f'Start update for: {from_currency}=>{to_currency}')
    xrate = XRate.select().where(XRate.from_currency == from_currency, XRate.to_currency == to_currency).first()
    log.debug(f'rate before: {xrate.rate}')
    xrate.rate = get_private_rate(from_currency)
    xrate.updated = peewee_datetime.datetime.now()
    xrate.save()
    log.debug(f'rate after: {xrate.rate}')
    log.info(f'Update finished for: {from_currency}=>{to_currency}')
    log.info('-------------------------------------')

def get_private_rate(from_currency):
    response_json = requests.get(url).json()
    log.debug(f'Privat response: {response_json}')
    usd_rate = find_usd_rate(response_json)
    return usd_rate

def find_usd_rate(response_data):
    for i in response_data:
        if i['ccy'] == 'USD':
            log.info(f'ccy(USD) was found: {float(i["sale"])}')
            return float(i['sale'])
    raise ValueError('Invalid Privat response: USD not found')



