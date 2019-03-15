from . import _Api


class Api(_Api):
    def __init__(self):
        super().__init__('privat_api')

    def _update_rate(self, xrate):
        return self._get_private_rate(xrate.from_currency)

    def _get_private_rate(self, from_currency):
        url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
        response = self._send_request(url=url, method='get')
        response_json = response.json()
        self.log.debug(f'Privat response: {response_json}')
        usd_rate = self._find_usd_rate(response_json, from_currency)
        return usd_rate

    def _find_usd_rate(self, response_data, from_currency):
        privat_aliases_map = {840: 'USD', 1000: 'BTC'}
        if from_currency not in privat_aliases_map:
            raise ValueError(f'Invalid from currency: {from_currency}')

        currency_alias = privat_aliases_map[from_currency]
        for i in response_data:
            if i['ccy'] == currency_alias:
                self.log.info(f'ccy(USD) was found: {float(i["sale"])}')
                return float(i['sale'])
        raise ValueError(f'Invalid Privat response: {currency_alias} not found')











