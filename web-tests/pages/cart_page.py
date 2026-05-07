from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_LIST = (By.CLASS_NAME, "cart_list")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    CART_CONTENTS_CONTAINER = (By.ID, "cart_contents_container")

    def is_loaded(self) -> bool:
        return self.is_visible(self.CART_CONTENTS_CONTAINER)

    def get_items_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def get_item_names(self) -> list[str]:
        elements = self.driver.find_elements(*self.ITEM_NAME)
        return [el.text for el in elements]

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)