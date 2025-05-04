# pages/inbox_page.py

from playwright._impl._locator import Locator
from playwright.sync_api import Page as PWPage
from pytest_playwright.pytest_playwright import context

from features.pages.base_page import BasePage
from utils.annotations import FindBy, Url, Action, Name


@Name("Inbox")
@Url("https://mail.centrum.sk/")
class InboxPage(BasePage):
    def __init__(self, page: PWPage):
        super().__init__(page)
        self.page = page

    @FindBy(xpath='//strong[@id="compose_button"]')
    def new_message_button(self) -> Locator:
        pass

    @FindBy(xpath='//form[@id="mail_composer_frm"]')
    def mail_composer_form_element(self) -> Locator:
        pass

    @FindBy(xpath='//input[@id="recipient_rightclick_to"]')
    def to_recipients_element(self) -> Locator:
        pass

    def wait_for_page_to_load(self):
        print("InboxPage loaded")
        self.new_message_button.wait_for(timeout=30000)
        print("InboxPage loaded")

    @Action("login")
    def login(self, data: dict):
        pass

