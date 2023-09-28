from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

feed_service_url = "http://127.0.0.1:5000"


@app.route('/feeds', methods=['GET'])
def forward_request():
    target_url = f"{feed_service_url}/feeds"
    response = requests.get(target_url, params=request.args)
    return (response.text, response.status_code, response.headers.items())


if __name__ == '__main__':
    app.run(debug=True)
