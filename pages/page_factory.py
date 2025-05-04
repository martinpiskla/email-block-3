# page_factory.py
import inspect
import features.pages  # adjust this if your pages are under a different module
from features.pages.base_page import BasePage
from features.pages.email_page import EmailPage
from features.pages.inbox_page import InboxPage

def get_all_page_classes():
    page_classes = []
    for name, obj in inspect.getmembers(features.pages, inspect.ismodule):
        for _, cls in inspect.getmembers(obj, inspect.isclass):
            if issubclass(cls, BasePage) and hasattr(cls, "_page_name"):
                page_classes.append(cls)
    return page_classes

class PageFactory:
    @staticmethod
    def get_page(name: str, playwright_page) -> BasePage:
        name = name.lower()
        for cls in get_all_page_classes():
            if cls._page_name == name:
                return cls(playwright_page)
        raise ValueError(f"No page class found for name: {name}")
