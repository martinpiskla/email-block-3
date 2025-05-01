# framework/config_loader.py
import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

with open(CONFIG_PATH, "r") as file:
    _config = yaml.safe_load(file)

def get_config_value(key: str):
    value = _config.get(key)
    if value is None:
        raise ValueError(f"Config key '{key}' is not found in config.yaml.")
    return value
