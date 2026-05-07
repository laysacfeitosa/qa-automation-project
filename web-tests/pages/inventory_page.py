from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")

    def is_loaded(self) -> bool:
        return self.is_visible(self.INVENTORY_CONTAINER)

    def get_product_count(self) -> int:
        return len(self.find_all(self.INVENTORY_ITEMS))

    def add_product_to_cart(self, product_name: str):
        slug = product_name.lower().replace(" ", "-")
        button = (By.ID, f"add-to-cart-{slug}")
        self.click(button)

    def remove_product_from_cart(self, product_name: str):
        slug = product_name.lower().replace(" ", "-")
        button = (By.ID, f"remove-{slug}")
        self.click(button)

    def get_cart_badge_count(self) -> int:
        if not self.is_visible(self.SHOPPING_CART_BADGE):
            return 0
        return int(self.get_text(self.SHOPPING_CART_BADGE))

    def open_cart(self):
        self.click(self.SHOPPING_CART_LINK)
