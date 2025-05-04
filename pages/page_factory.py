# pages/page_factory.py
from features.pages.inbox_page import InboxPage
from features.pages.email_page import EmailPage

class PageFactory:
    page_map = {
        "Email": EmailPage,
        "Inbox": InboxPage,
        # Add other mappings here
    }

    @staticmethod
    def get_page(name: str, playwright_page):
        page_class = PageFactory.page_map.get(name)
        if not page_class:
            raise ValueError(f"No page class found for name: {name}")
        return page_class(playwright_page)
