from models import XRate, peewee_datetime
from config import logging, LOGGER_CONFIG
import requests
import xml.etree.ElementTree as ET

log = logging.getLogger('cbr_api')
fh = logging.FileHandler(LOGGER_CONFIG['file'])
fh.setLevel(LOGGER_CONFIG['level'])
fh.setFormatter(LOGGER_CONFIG['formatter'])
log.addHandler(fh)
log.setLevel(LOGGER_CONFIG['level'])

url = 'http://www.cbr.ru/scripts/XML_daily.asp'

def update_xrates(from_currency, to_currency):
    log.info(f'Start update for: {from_currency}=>{to_currency}')
    xrate = XRate.select().where(XRate.from_currency == from_currency, XRate.to_currency == to_currency).first()
    log.debug(f'rate before: {xrate.rate}')
    xrate.rate = get_cbr_rate(from_currency)
    xrate.updated = peewee_datetime.datetime.now()
    xrate.save()
    log.debug(f'rate after: {xrate.rate}')
    log.info(f'Update finished for: {from_currency}=>{to_currency}')
    log.info('*************************************')


def get_cbr_rate(from_currency):
    response = requests.get(url)
    log.debug(f'response.encoding: {response.encoding}')
    response_text = response.text
    log.debug(f'response.text: {response_text}')
    usd_rate = find_usd_rate(response_text)
    return usd_rate

def find_usd_rate(response_text):
    root = ET.fromstring(response_text)
    valutes = root.findall('Valute')

    for valute in valutes:
        if valute.find('CharCode').text == 'USD':
            print(valute)
            return float(valute.find('Value').text.replace(',', '.'))
    raise ValueError('Invalid Cbr response: USD not found!')























