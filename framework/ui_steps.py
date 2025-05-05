from pytest_bdd import given, when, then, parsers
from features.support.context import context
from framework.pages.page_factory import PageFactory

@when(parsers.re(r'I click on (?P<element_name>.*) (?P<element_type>button|element|link|field)'))
def click_on_element(element_name, element_type):
    page_object = context["current_page"]
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
    page = browser_context.pages[-1]
    # Get the page object for the specified page name
    page_object = PageFactory.get_page(page_name, page)
    # Update the current page in the context
    context["current_page"] = page_object

    # Wait for the page to load
    page_object.wait_for_page_to_load()

@then(parsers.re(r'(?P<element_name>.*) (?P<element_type>button|element|link|field) is visible'))
def element_is_visible(element_name, element_type):
    page_object = context["current_page"]
    # Build the attribute name dynamically (e.g., "submit_button")
    attribute_name = f"{element_name.lower().replace(' ', '_')}_{element_type.lower()}"

    # Get the element
    element = getattr(page_object, attribute_name, None)

    element.wait_for(timeout=30000)

    if not element:
        raise AttributeError(f"Element '{attribute_name}' not found on {type(page_object).__name__}")

    # Check visibility
    if not element.is_visible():
        raise AssertionError(f"Element '{attribute_name}' is not visible on {type(page_object).__name__}")


@given(parsers.re(r'I open (?P<page_name>.+) page'))
def open_page(page_name, browser_context):
    page = browser_context.new_page()
    page_object = PageFactory.get_page(page_name, page)

    context["current_page"] = page_object  # <-- store PO globally

    page.goto(page_object.url)
    page_object.wait_for_page_to_load()