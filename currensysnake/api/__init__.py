import traceback
import requests

from models import XRate, peewee_datetime, ApiLog, ErrorLog
from config import logging, LOGGER_CONFIG, HTTP_TIMEOUT


fh = logging.FileHandler(LOGGER_CONFIG['file'])
fh.setLevel(LOGGER_CONFIG['level'])
fh.setFormatter(LOGGER_CONFIG['formatter'])


class _Api:
    def __init__(self, logger_name):
        self.log = logging.getLogger(logger_name)
        self.log.addHandler(fh)
        self.log.setLevel(LOGGER_CONFIG['level'])

    def update_rate(self, from_currency, to_currency):
        self.log.info(f'Start update for: {from_currency}=>{to_currency}')
        xrate = XRate.select().where(XRate.from_currency == from_currency, XRate.to_currency == to_currency).first()
        self.log.debug(f'rate before: {xrate.rate}')
        xrate.rate = self._update_rate(xrate)
        xrate.updated = peewee_datetime.datetime.now()
        xrate.save()
        self.log.debug(f'rate after: {xrate.rate}')
        self.log.info(f'Update finished for: {from_currency}=>{to_currency}')
        self.log.info('*************************************')

    def _update_rate(self, xrate):
        raise NotImplementedError('_update_rate')

    def _send_request(self, url, method, data=None, headers=None):
        api_log = ApiLog(request_url=url, request_data=data, request_method=method, request_headers=headers)
        try:
            response = self._send(method=method, url=url, headers=headers, data=data)
            api_log.response_text = response.text
            return response
        except Exception as ex:
            self.log.exception('Error during request sending')
            api_log.error = str(ex)
            ErrorLog.create(request_data=data, request_url=url, request_method=method, error=str(ex),
                            traceback=traceback.format_exc(chain=False))
            raise
        finally:
            api_log.finished = peewee_datetime.datetime.now()
            api_log.save()

    def _send(self, url, method, data=None, headers=None):
        return requests.request(method=method, url=url, headers=headers, data=data, timeout=HTTP_TIMEOUT)
























