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
    return controllers.GetApiRates().call(mft)

@app.route('/update/<int:from_currency>/<int:to_currency>')
@app.route('/update/all')
def update_xrates(from_currency=None, to_currency=None):
    return controllers.UpdateRates().call(from_currency, to_currency)



@app.route('/logs')
def view_logs():
    return controllers.ViewLogs().call()

