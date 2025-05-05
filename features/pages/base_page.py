from charset_normalizer.md import annotations


class BasePage:
    def __init__(self, page):
        self.page = page

    def click(self, selector: str):
        self.page.locator(selector).click()

    def fill(self, selector: str, text: str):
        self.page.locator(selector).fill(text)

    def get_text(self, selector: str):
        return self.page.locator(selector).inner_text()

    def wait_for_selector(self, selector: str, timeout: int = 5000):
        self.page.wait_for_selector(selector, timeout=timeout)

    def execute_action(self, action_name: str, data: dict):
        action = annotations.get(action_name.lower())
        if not action:
            raise Exception(f"Action '{action_name}' not registered.")
        return action(self, data)

    def wait_for_page_to_load(self):
        pass