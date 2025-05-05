import datetime

def get_current_timestamp() -> str:
    """Returns the current timestamp in the format 'DD-MM-YYYY-HH-mm-ss'."""
    return datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")