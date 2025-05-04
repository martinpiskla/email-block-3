# utils/annotations.py
from framework.variable_resolver import resolve_dynamic_variable
from playwright.sync_api import Locator

def Name(name: str):
    def decorator(cls):
        cls.__name__ = name
        return cls
    return decorator

def Url(url: str):
    def decorator(cls):
        # Try resolving if dynamic variable
        try:
            context = {}  # You can later inject context here for $Var if needed
            resolved_url = resolve_dynamic_variable(url, context)
        except Exception:
            resolved_url = url  # Use raw string if resolution fails
        cls.url = resolved_url
        return cls
    return decorator

# framework/annotations.py

def FindBy(**kwargs):
    def decorator(func):
        selector = build_selector(**kwargs)
        def wrapper(self) -> Locator:
            return self.page.locator(selector)
        return property(wrapper)
    return decorator

def build_selector(**kwargs):
    if 'xpath' in kwargs:
        return kwargs['xpath']
    elif 'css' in kwargs:
        return kwargs['css']
    elif 'text' in kwargs:
        return f"text={kwargs['text']}"
    elif 'id' in kwargs:
        return f"#{kwargs['id']}"
    elif 'data_test_id' in kwargs:
        return f"[data-testid='{kwargs['data_test_id']}']"
    else:
        raise ValueError("Unsupported locator type.")

def Action(name):
    def decorator(func):
        func._action_name = name.lower()
        return func
    return decorator

def find_action_method(page_obj, action_name: str):
    for attr in dir(page_obj):
        method = getattr(page_obj, attr)
        if callable(method) and getattr(method, "_action_name", None) == action_name.lower():
            return method
    return None
