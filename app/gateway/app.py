from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from routes import auth
app.register_blueprint(auth.bp)

from routes import feeds
app.register_blueprint(feeds.bp)

from routes import forecast
app.register_blueprint(forecast.bp)

if __name__ == '__main__':
    app.run(debug=True)
