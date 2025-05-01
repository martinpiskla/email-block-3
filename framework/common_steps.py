# framework/common_steps.py
from pytest_bdd import given, when, then, parsers
import re

from framework.env_loader import get_env_variable
from framework.config_loader import get_config_value


def resolve_dynamic_variable(full_key: str, context: dict) -> str:
    """Resolves $Env.XXX, $Config.XXX, or $Var.XXX variables."""
    if full_key.startswith("Env."):
        return get_env_variable(full_key[4:])
    elif full_key.startswith("Config."):
        return get_config_value(full_key[7:])
    elif full_key.startswith("Var."):
        key = full_key[4:]
        if key not in context:
            raise ValueError(f"$Var.{key} not found in context.")
        return context[key]
    else:
        raise ValueError(f"Unknown variable source: {full_key}")

@given(parsers.re(r"I print \$(?P<var_type>Env|Config|Var)\.(?P<key>\w+) variable content"))
@when(parsers.re(r"I print \$(?P<var_type>Env|Config|Var)\.(?P<key>\w+) variable content"))
@then(parsers.re(r"I print \$(?P<var_type>Env|Config|Var)\.(?P<key>\w+) variable content"))
def print_variable(var_type, key, context):
    full_key = f"{var_type}.{key}"
    value = resolve_dynamic_variable(full_key, context)
    print(f"{full_key} = {value}")

@given("I go to the login page")
def go_to_login_page():
    print("Navigating to the login page")

@when("I fill in login details")
def fill_in_login_details():
    print("Filling in login details")

@then("I am logged in")
def verify_logged_in():
    print("User is logged in")

def interpolate_vars_in_string(text: str, context: dict) -> str:
    """Replace all $Var.xxx patterns in a string using context."""
    def replacer(match):
        var_name = match.group(1)
        if var_name not in context:
            raise ValueError(f"$Var.{var_name} not found in context for interpolation.")
        return str(context[var_name])

    return re.sub(r"\$Var\.([a-zA-Z_]\w*)", replacer, text)

@given(parsers.re(r'I save (?P<value>.+?) as \$Var\.(?P<var_key>\w+) variable'))
@when(parsers.re(r'I save (?P<value>.+?) as \$Var\.(?P<var_key>\w+) variable'))
@then(parsers.re(r'I save (?P<value>.+?) as \$Var\.(?P<var_key>\w+) variable'))
def save_var_value(value, var_key, context):
    value = interpolate_vars_in_string(value, context)
    context[var_key] = value
    print(f'Saved $Var.{var_key} = {value}')

@given(parsers.re(r'I say "(?P<text>.+)"'))
def say_step(text, context):
    message = interpolate_vars_in_string(text, context)
    print(f"Message: {message}")

@then(parsers.re(r'I say (?P<text>.+)'))
def say_step_unquoted(text, context):
    message = interpolate_vars_in_string(text, context)
    print(f"Message: {message}")

