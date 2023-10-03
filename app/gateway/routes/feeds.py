from flask import Blueprint, request
import requests

from config import config
from auth import client as auth

API_PATH = "/api/v1"
bp = Blueprint("feeds", __name__)


@bp.get(f'{API_PATH}/feeds')
@auth.authenticated
def forward_feeds():
    target_url = f"{config.feed_service_url}/feeds"
    response = requests.get(target_url, params=request.args)
    return (response.text, response.status_code, response.headers.items())
