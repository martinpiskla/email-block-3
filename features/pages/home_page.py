# pages/home_page.py
import time
from os import getenv

from playwright._impl._locator import Locator
from playwright.sync_api import Page as PWPage

from features.pages.base_page import BasePage
from framework.variable_resolver import resolve_dynamic_variable
from utils.annotations import FindBy, Url, Action, Name


@Name("Home")
@Url("$Env.EMAIL_URL")
class HomePage(BasePage):
    def __init__(self, page: PWPage):
        super().__init__(page)
        self.page = page

    @FindBy(xpath='//div[@class="MailBoxCentrum_aside-email-form__nxE3J"]/descendant::input[@name="userName"]')
    def email_input(self) -> Locator:
        pass

    @FindBy(xpath='//div[@class="MailBoxCentrum_aside-email-form__nxE3J"]/descendant::input[@name="password"]')
    def password_input(self) -> Locator:
        pass

    @FindBy(xpath='//div[@class="MailBoxCentrum_aside-email-form__nxE3J"]/descendant::button[@type="submit" and contains(text(),"Prihlásiť")]')
    def login_button(self) -> Locator:
        pass

    @FindBy(xpath='//button[@id="onetrust-accept-btn-handler"]')
    def accept_cookies_button(self) -> Locator:
        pass

    @FindBy(xpath=f'//aside/descendant::a[@href="https://mail.centrum.sk" and contains(text(),"{resolve_dynamic_variable("$Env.EMAIL_USERNAME", {})}")]')
    def access_inbox_button(self) -> Locator:
        pass

    def wait_for_page_to_load(self):
        self.login_button.wait_for(timeout=10000)

        try:
            # Attempt to wait for the accept cookies button
            self.accept_cookies_button.wait_for(timeout=10000)
            if self.accept_cookies_button.is_visible():
                self.accept_cookies_button.click()
        except Exception:
            # If not visible or timeout occurs, just continue, no need to accept cookies
            pass

    @Action("login")
    def login(self, data: dict):
        self.email_input.fill(data["Username"])
        self.password_input.fill(data["Password"])
        self.login_button.click()
        self.access_inbox_button.wait_for(timeout=10000)
        self.access_inbox_button.click()