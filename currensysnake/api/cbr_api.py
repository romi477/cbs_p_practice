import xml.etree.ElementTree as ET
from . import _Api


class CbrApi(_Api):
    def __init__(self):
        super().__init__('cbr_api')

    def _update_rate(self, xrate):
        return self._update_cbr_rate(xrate.from_currency)

    def _update_cbr_rate(self, from_currency):
        url = 'http://www.cbr.ru/scripts/XML_daily.asp'
        response = self._send_request(url=url, method='get')
        self.log.debug(f'response.encoding: {response.encoding}')
        response_text = response.text
        self.log.debug(f'response.text: {response_text}')
        usd_rate = self._find_rate(response_text, from_currency)
        return usd_rate

    def _find_rate(self, response_text, from_currency):
        root = ET.fromstring(response_text)
        valutes = root.findall('Valute')

        cbr_valute_map = {840: "USD", 980: "UAH"}
        currency_cbr_alias = cbr_valute_map[from_currency]

        for valute in valutes:
            if valute.find('CharCode').text == currency_cbr_alias:
                return float(valute.find('Value').text.replace(',', '.'))
        raise ValueError('Invalid Cbr response: USD not found!')




























