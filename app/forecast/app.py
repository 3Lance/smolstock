import yfinance as yf
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/forecast")
def index():
    return jsonify({"res": "Hello World"})

if __name__ == "__main__":
    app.run(debug=True, port=1235)
