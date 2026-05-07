from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_LIST = (By.CLASS_NAME, "cart_list")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def is_loaded(self) -> bool:
        return self.is_visible(self.CART_LIST)

    def get_items_count(self) -> int:
        if not self.is_loaded():
            return 0
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def get_item_names(self) -> list[str]:
        return [el.text for el in self.find_all(self.ITEM_NAME)]

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
