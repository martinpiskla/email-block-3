# pages/gmail_page.py
import time

from playwright._impl._locator import Locator
from playwright.sync_api import Page as PWPage

from features.pages.base_page import BasePage
from utils.annotations import Name, FindBy, Url, Action


@Name("Gmail")
@Url("$Env.GMAIL_URL")
class GmailPage(BasePage):
    def __init__(self, page: PWPage):
        super().__init__(page)
        self.page = page

    @FindBy(xpath='//input[@id="identifierId"]')
    def email_input(self) -> Locator:
        pass

    @FindBy(xpath='//span[contains(text(),"Ďalej")]/ancestor::button')
    def next_button(self) -> Locator:
        pass

    def wait_for_page_to_load(self):
        self.next_button.wait_for(timeout=10000)

    @Action("login")
    def login(self, data: dict):
        self.email_input.fill(data["Username"])
        self.next_button.click()