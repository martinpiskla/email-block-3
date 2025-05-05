# framework/env_loader.py
import os
from dotenv import load_dotenv

# Load the .env file once, early in the test lifecycle
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path, override=True)

def get_env_variable(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' is not set in .env or system.")
    return value
