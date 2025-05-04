# framework/common_steps.py
from charset_normalizer.md import annotations
from pytest_bdd import given, when, then, parsers
import re
from features.support.context import context
from features.pages.gmail_page import GmailPage
from pages.page_factory import PageFactory
from framework.variable_resolver import resolve_dynamic_variable
from typing import List

from utils.annotations import find_action_method


@given(parsers.re(r"I print (?P<var_type>\$Env|\$Config|\$Var)(?P<key>\.\w+) variable content"))
@when(parsers.re(r"I print (?P<var_type>\$Env|\$Config|\$Var)(?P<key>\.\w+) variable content"))
@then(parsers.re(r"I print (?P<var_type>\$Env|\$Config|\$Var)(?P<key>\.\w+) variable content"))
def print_variable(var_type, key, context):
    full_key = f"{var_type}{key}"
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

    return re.sub(r"(\$Var\.([a-zA-Z_]\w*))", replacer, text)

@given(parsers.re(r'I save (?P<value>.+?) as (?P<var_key>\$Var\.\w+) variable'))
@when(parsers.re(r'I save (?P<value>.+?) as (?P<var_key>\$Var\.\w+) variable'))
@then(parsers.re(r'I save (?P<value>.+?) as (?P<var_key>\$Var\.\w+) variable'))
def save_var_value(value, var_key, context):
    value = interpolate_vars_in_string(value, context)
    context[var_key] = value
    print(f'Saved {var_key} = {value}')

@given(parsers.re(r'I say "(?P<text>.+)"'))
def say_step(text, context):
    message = interpolate_vars_in_string(text, context)
    print(f"Message: {message}")

@then(parsers.re(r'I say (?P<text>.+)'))
def say_step_unquoted(text, context):
    message = interpolate_vars_in_string(text, context)
    print(f"Message: {message}")

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
def execute_action_by_name(action_name, page_object, context):
    method = find_action_method(page_object, action_name)
    data = context.table[0]
    print(data)
    if not method:
        raise Exception(f"No method found with @Action('{action_name}') on {type(page_object).__name__}")
    return method(data)