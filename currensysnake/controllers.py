from flask import render_template, make_response, jsonify, request, redirect
import xmltodict

from models import XRate, ApiLog
import api


class BaseController:
    def __init__(self):
        self.request = request

    def call(self, *args, **kwargs):
        try:
            return self._call(*args, **kwargs)
        except Exception as ex:
            raise make_response(str(ex), 500)

    def _call(self, *args, **kwargs):
        raise NotImplementedError('_call')

class ViewAllRates(BaseController):
    def _call(self):
        xrates = XRate.select()
        return render_template('xrates.html', xrates=xrates)

class GetApiRates(BaseController):
    def _call(self, fmt):
        xrates = XRate.select()
        xrates = self._filter(xrates)

        if fmt == 'json':
            return self._get_json(xrates)
        elif fmt == 'xml':
            return self._get_xml(xrates)
        raise ValueError(f'Unknown fmt: {fmt}')

    def _filter(self, xrates):
        args = self.request.args

        if 'from_currency' in args:
            xrates = xrates.where(XRate.from_currency == args['from_currency'])
        if 'to_currency' in args:
            xrates = xrates.where(XRate.to_currency == args['to_currency'])
        return xrates

    def _get_xml(self, xrates):
        d = {'xrates': {'xrate': [
            {'from': rate.from_currency, 'to': rate.to_currency} for rate in xrates]}}
        return make_response(xmltodict.unparse(d), {'Content-Type': 'text/xml'})

    def _get_json(self, xrates):
        return jsonify([{'from': rate.from_currency, 'to': rate.to_currency, 'rate': rate.rate} for rate in xrates])

class UpdateRates(BaseController):
    def _call(self, from_currency, to_currency):
        if not from_currency and not to_currency:
            self._update_all()
        elif from_currency and to_currency:
            self._update_rate(from_currency, to_currency)
        else:
            raise ValueError('from_currency and to_currency')
        return redirect('/xrates')

    def _update_rate(self, from_currency, to_currency):
        api.update_rate(from_currency, to_currency)

    def _update_all(self):
        xrates = XRate.select()
        for rate in xrates:
            try:
                self._update_rate(rate.from_currency, rate.to_currency)
            except Exception as ex:
                print(ex)

class ViewLogs(BaseController):
    def _call(self):
        page = int(self.request.args.get('page', 1))
        logs = ApiLog.select().paginate(page, 10).order_by(ApiLog.id.desc())
        return render_template('logs.html', logs=logs)













