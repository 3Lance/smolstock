from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

feed_service_url = "http://127.0.0.1:1234"
forecast_service_url = "http://127.0.0.1:1235"

@app.route('/feeds', methods=['GET'])
def forward_feeds():
    target_url = f"{feed_service_url}/feeds"
    response = requests.get(target_url, params=request.args)
    return (response.text, response.status_code, response.headers.items())

@app.route("/forecast", methods=['GET'])
def forward_forecast():
    target_url = f"{forecast_service_url}/forecast"
    response = requests.get(target_url, params=request.args)
    return (response.text, response.status_code, response.headers.items())

if __name__ == '__main__':
    app.run(debug=True)
