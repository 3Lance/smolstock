from dacite import from_dict
from dataclasses import dataclass
from typing import Optional
import yaml


@dataclass
class Config:
    feed_service_url: str
    forecast_service_url: str
    auth_service_url: str
    secret_key: str


def load_config(path: str) -> Optional[Config]:
    with open(path, "r") as f:
        try:
            return from_dict(data=yaml.safe_load(f), data_class=Config)
        except yaml.YAMLError:
            return None


config = load_config("./config.yaml")
