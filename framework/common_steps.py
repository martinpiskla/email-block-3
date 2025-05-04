# framework/common_steps.py
from pytest_bdd import given, when, then, parsers
import re
from features.support.context import context
from pages.page_factory import PageFactory
from framework.variable_resolver import resolve_dynamic_variable
from utils.annotations import find_action_method

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

@given(parsers.re(r'I open (?P<page_name>.+) page'))
def open_page(page_name, browser_context):
    page = browser_context.new_page()
    page_object = PageFactory.get_page(page_name, page)

    context["current_page"] = page_object  # <-- store PO globally

    page.goto(page_object.url)
    page_object.wait_for_page_to_load()

@when(parsers.re(r'I execute (?P<action_name>\w+)$'))
def execute_action_by_name(action_name, page_object):
    method = find_action_method(page_object, action_name)
    if not method:
        raise Exception(f"No method found with @Action('{action_name}') on {type(page_object).__name__}")
    return method()

@when(parsers.re(r'I execute (?P<action_name>\w+) with:$'))
def execute_action_by_name_with_datatable(action_name, page_object, datatable):
    method = find_action_method(page_object, action_name)
    if not method:
        raise Exception(f"No method found with @Action('{action_name}') on {type(page_object).__name__}")

    # Convert list of lists to a dict
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

@when(parsers.re(r'I click on (?P<element_name>.*) (?P<element_type>button|element|link)'))
def click_on_element(element_name, element_type, page_object):
    # Replace spaces with underscores and construct the attribute name dynamically
    attribute_name = f"{element_name.lower().replace(' ', '_')}_{element_type.lower()}"

    # Retrieve the element from the current page object
    element = getattr(page_object, attribute_name, None)

    if not element:
        raise AttributeError(f"Element '{attribute_name}' not found on {type(page_object).__name__}")

    # Perform the click action
    element.click()

@then(parsers.re(r'I am on (?P<page_name>.+) page'))
def landed_on_page(page_name, browser_context):
    # Retrieve the current page from the context
    current_page = context.get("current_page").page

    # Get the page object for the specified page name
    page_object = PageFactory.get_page(page_name, current_page)

    # Update the current page in the context
    context["current_page"] = page_object

    # Wait for the page to load
    page_object.wait_for_page_to_load()