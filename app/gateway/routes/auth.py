from flask import Blueprint, request
import requests

from config import config


API_PATH = "/api/v1"
bp = Blueprint("auth", __name__)


@bp.post(f"{API_PATH}/register")
def forward_register():
    target_url = f"{config.auth_service_url}/register"
    response = requests.post(
        url=target_url,
        data=request.get_data().decode(),
        headers={
            'Content-Type': 'application/json'
        },
    )
    return (response.text, response.status_code, response.headers.items())


@bp.post(f"{API_PATH}/login")
def forward_login():
    target_url = f"{config.auth_service_url}/login"
    response = requests.post(
        url=target_url,
        data=request.get_data().decode(),
        headers={
            'Content-Type': 'application/json'
        },
    )
    return (response.text, response.status_code, response.headers.items())
