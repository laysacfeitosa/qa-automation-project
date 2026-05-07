from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    SUMMARY_SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    SUMMARY_TAX = (By.CLASS_NAME, "summary_tax_label")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CHECKOUT_ITEMS = (By.CLASS_NAME, "cart_item")

    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def get_subtotal(self) -> float:
        text = self.get_text(self.SUMMARY_SUBTOTAL)
        return float(text.split("$")[1])

    def get_total(self) -> float:
        text = self.get_text(self.SUMMARY_TOTAL)
        return float(text.split("$")[1])

    def get_items_in_summary(self) -> int:
        return len(self.find_all(self.CHECKOUT_ITEMS))

    def finish_purchase(self):
        self.click(self.FINISH_BUTTON)

    def is_purchase_complete(self) -> bool:
        return self.is_visible(self.COMPLETE_HEADER)

    def get_completion_message(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)

    def back_to_products(self):
        self.click(self.BACK_HOME_BUTTON)
