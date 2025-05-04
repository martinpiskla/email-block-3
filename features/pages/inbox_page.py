# pages/inbox_page.py
import time

from playwright._impl._locator import Locator
from playwright.sync_api import Page as PWPage
from pytest_playwright.pytest_playwright import context

from features.pages.base_page import BasePage
from utils.annotations import FindBy, Url, Action, Name
from utils.file_utils import read_attachment, read_file_path


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

    @FindBy(xpath='//li[@id="qabook_switch_names"]')
    def select_contacts_button(self) -> Locator:
        pass

    @FindBy(xpath='//span[contains(text()," Martin Piskla ")]')
    def saved_contact_element(self) -> Locator:
        pass

    @FindBy(xpath='//div[@class="recipient-address recipient-block" and contains(text(),"Martin Piskla")]')
    def saved_contact_in_to_recipients_element(self) -> Locator:
        pass

    @FindBy(xpath='//input[@id="subject_input"]')
    def input_field(self) -> Locator:
        pass

    @FindBy(xpath='//body[@id="tinymce"]')
    def input_body(self) -> Locator:
        pass

    @FindBy(xpath='//input[@id="mc_attachments_add"]')
    def input_attachment(self) -> Locator:
        pass

    @FindBy(xpath='//a[@id="qa_email_send_upper"]//strong')
    def send_email_button(self) -> Locator:
        pass

    @FindBy(xpath='//a[@id="qa_logout_ju2"]/parent::li')
    def logout_button(self) -> Locator:
        pass

    def wait_for_page_to_load(self):
        print("InboxPage loaded")
        self.new_message_button.wait_for(timeout=30000)
        print("InboxPage loaded")

    @Action("write email and add attachment")
    def write_email(self, data: dict):
        subject_text = read_attachment(data.get("Subject", ""))
        self.input_field.fill(subject_text)
        self.input_attachment.set_input_files(read_file_path(data["Attachment"]))

    @Action("logout")
    def logout(self):
        time.sleep(10000)

