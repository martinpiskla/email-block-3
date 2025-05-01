
from .base_page import BasePage

class ExamplePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def click_login_button(self):
        self.click("#login-button")

    def enter_username(self, username):
        self.fill("#username", username)

    def enter_password(self, password):
        self.fill("#password", password)
