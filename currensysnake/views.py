from flask import request

from app import app
import controllers

@app.route('/')
def hello():
    return 'Hello mate!'

@app.route('/xrates')
def view_rates():
    return controllers.ViewAllRates().call()

@app.route('/api/xrates/<mft>')
def api_rates(mft):
    return f'Rates with format: {mft}. Args: {request.args}'