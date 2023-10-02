import yfinance as yf
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route("/forecast")
def index():
    tick = request.args.get("q")

    if not tick:
        return jsonify({"error": "no stock provided"})

    stock = yf.Ticker(tick)
    hist = stock.history(period="1mo")
    return hist.to_json()

if __name__ == "__main__":
    app.run(debug=True, port=1235)
