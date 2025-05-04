# pages/page_factory.py
from features.pages.gmail_page import GmailPage

class PageFactory:
    page_map = {
        "Gmail": GmailPage,
        # Add other mappings here
    }

    @staticmethod
    def get_page(name: str, playwright_page):
        page_class = PageFactory.page_map.get(name)
        if not page_class:
            raise ValueError(f"No page class found for name: {name}")
        return page_class(playwright_page)
