from flask import Blueprint, request
import requests

from config import config
from auth import client as auth


API_PATH = "/api/v1"
bp = Blueprint("forecast", __name__)


@bp.get("/forecast")
@bp.get("/forecast/<path:path>")
@auth.authenticated
def forward_forecast(path=''):
    target_url = f"{config.forecast_service_url}/forecast" + path
    response = requests.get(target_url, params=request.args)
    return (response.text, response.status_code, response.headers.items())
