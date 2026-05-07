import pytest
from pages.cart_page import CartPage


@pytest.mark.cart
class TestCart:

    def test_add_single_product_to_cart(self, driver, logged_in_inventory):
        logged_in_inventory.add_product_to_cart("Sauce Labs Backpack")
        assert logged_in_inventory.get_cart_badge_count() == 1

    def test_add_multiple_products_to_cart(self, driver, logged_in_inventory):
        products = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        for product in products:
            logged_in_inventory.add_product_to_cart(product)

        assert logged_in_inventory.get_cart_badge_count() == 3

    def test_remove_product_from_cart(self, driver, logged_in_inventory):
        logged_in_inventory.add_product_to_cart("Sauce Labs Backpack")
        assert logged_in_inventory.get_cart_badge_count() == 1

        logged_in_inventory.remove_product_from_cart("Sauce Labs Backpack")
        assert logged_in_inventory.get_cart_badge_count() == 0

    def test_cart_persists_added_items(self, driver, logged_in_inventory):
        logged_in_inventory.add_product_to_cart("Sauce Labs Backpack")
        logged_in_inventory.add_product_to_cart("Sauce Labs Bike Light")
        logged_in_inventory.open_cart()

        cart = CartPage(driver)
        assert cart.is_loaded()
        assert cart.get_items_count() == 2

        names = cart.get_item_names()
        assert "Sauce Labs Backpack" in names
        assert "Sauce Labs Bike Light" in names
