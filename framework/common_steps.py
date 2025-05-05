# framework/common_steps.py
from pytest_bdd import given, when, then, parsers
import re
from features.support.context import context
from framework.variable_resolver import resolve_dynamic_variable
from framework.utils.annotations import find_action_method


@given(parsers.re(r"I print (?P<var_type>\$Env|\$Config|\$Var)(?P<key>\.\w+) variable content"))
@when(parsers.re(r"I print (?P<var_type>\$Env|\$Config|\$Var)(?P<key>\.\w+) variable content"))
@then(parsers.re(r"I print (?P<var_type>\$Env|\$Config|\$Var)(?P<key>\.\w+) variable content"))
def print_variable(var_type, key, context):
    full_key = f"{var_type}{key}"
    value = resolve_dynamic_variable(full_key, context)
    print(f"{full_key} = {value}")

def interpolate_vars_in_string(text: str, context: dict) -> str:
    """Replace all $Var.xxx patterns in a string using context."""
    def replacer(match):
        var_name = match.group(1)
        if var_name not in context:
            raise ValueError(f"$Var.{var_name} not found in context for interpolation.")
        return str(context[var_name])

    return re.sub(r"(\$Var\.([a-zA-Z_]\w*))", replacer, text)

@given(parsers.re(r'I save (?P<value>.+?) as (?P<var_key>\$Var\.\w+) variable'))
@when(parsers.re(r'I save (?P<value>.+?) as (?P<var_key>\$Var\.\w+) variable'))
@then(parsers.re(r'I save (?P<value>.+?) as (?P<var_key>\$Var\.\w+) variable'))
def save_var_value(value, var_key, context):
    value = interpolate_vars_in_string(value, context)
    context[var_key] = value
    print(f'Saved {var_key} = {value}')


@when(parsers.re(r'I execute (?P<action_name>.+)$'))
@then(parsers.re(r'I execute (?P<action_name>.+)$'))
def execute_action_by_name(action_name):
    page_object = context["current_page"]
    method = find_action_method(page_object, action_name)
    if not method:
        raise Exception(f"No method found with @Action('{action_name}') on {type(page_object).__name__}")
    return method()


@when(parsers.re(r'I execute (?P<action_name>.+?) with:$'))
def execute_action_by_name_with_datatable(action_name, datatable):
    page_object = context["current_page"]
    method = find_action_method(page_object, action_name)
    if not method:
        raise Exception(f"No method found with @Action('{action_name}') on {type(page_object).__name__}")

    # Convert list of lists to dict
    try:
        data = dict(datatable)
    except Exception as e:
        raise ValueError(f"Failed to convert datatable to dict: {e}\nActual datatable: {datatable}")

    # Resolve dynamic variables
    resolved_data = {
        key: resolve_dynamic_variable(value, context={}) if isinstance(value, str) and value.startswith("$") else value
        for key, value in data.items()
    }

    return method(resolved_data)


