from framework.env_loader import get_env_variable
from framework.config_loader import get_config_value

def resolve_dynamic_variable(full_key: str, context: dict) -> str:
    """Resolves $Env.XXX, $Config.XXX, or $Var.XXX variables."""
    if full_key.startswith("$Env."):
        return get_env_variable(full_key[5:])
    elif full_key.startswith("$Config."):
        return get_config_value(full_key[8:])
    elif full_key.startswith("$Var."):
        key = full_key[5:]
        if key not in context:
            raise ValueError(f"$Var.{key} not found in context.")
        return context[key]
    else:
        raise ValueError(f"Unknown variable source: {full_key}")