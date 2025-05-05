# pages/inbox_page.py
import time

from playwright._impl._locator import Locator
from playwright.sync_api import Page as PWPage
from pytest_playwright.pytest_playwright import context

from features.pages.base_page import BasePage
from framework.variable_resolver import resolve_dynamic_variable
from framework.utils.annotations import FindBy, Url, Action, Name
from framework.utils.file_utils import read_attachment, read_file_path, write_to_file
from framework.utils.time_utils import get_current_timestamp


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

    @FindBy(xpath=f'//span[contains(text()," {resolve_dynamic_variable("$Env.CONTACT_FULLNAME", {})} ")]')
    def saved_contact_element(self) -> Locator:
        pass

    @FindBy(xpath=f'//div[@class="recipient-address recipient-block" and contains(text(),"{resolve_dynamic_variable("$Env.CONTACT_FULLNAME", {})}")]')
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

    @FindBy(xpath='//a[@id="fld_1_line"]/span[contains(text(),"Odoslaná")]')
    def sent_folder_element(self) -> Locator:
        pass

    def wait_for_page_to_load(self):
        print("InboxPage loaded")
        self.new_message_button.wait_for(timeout=30000)
        print("InboxPage loaded")

    @Action("write email and add attachment")
    def write_email(self, data: dict):
        write_to_file(data.get("Subject", ""), get_current_timestamp())
        subject_text = read_attachment(data.get("Subject", ""))
        self.input_field.fill(subject_text)
        self.input_attachment.set_input_files(read_file_path(data["Attachment"]))
        time.sleep(5) #for visual check


    @Action("validate email is in sent folder")
    def validate_email_was_sent(self):
        self.sent_folder_element.click()
        sent_email_subject = self.page.locator(f'//div[contains(text(),"{read_attachment("testEmailSubject.txt")}")]')
        sent_email_subject.wait_for(timeout=10000)
        time.sleep(5) #for visual check
        assert sent_email_subject.is_visible(), "Email was not sent successfully"
