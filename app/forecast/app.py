import yfinance as yf
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route("/forecast")
def index():
    stock = yf.Ticker('AMZN')
    hist = stock.history() #dati dell'ultimo anno

    json_data = hist.reset_index().to_json(orient='records', date_format='iso')
    json_data = json.loads(json_data)
    df = pd.DataFrame(json_data)
    df=df[['Date', 'Close']]

    return df.to_json()

if __name__ == "__main__":
    app.run(debug=True, port=1235)
