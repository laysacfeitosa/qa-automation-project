import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.config import USERS, CHECKOUT_INFO


@pytest.mark.checkout
class TestCheckoutInformation:

    def test_checkout_requires_first_name(self, driver, logged_in_inventory):
        logged_in_inventory.add_product_to_cart("Sauce Labs Backpack")
        logged_in_inventory.open_cart()
        CartPage(driver).proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_information("", "Silva", "60000-000")
        assert "First Name is required" in checkout.get_error_message()

    def test_checkout_requires_last_name(self, driver, logged_in_inventory):
        logged_in_inventory.add_product_to_cart("Sauce Labs Backpack")
        logged_in_inventory.open_cart()
        CartPage(driver).proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_information("João", "", "60000-000")
        assert "Last Name is required" in checkout.get_error_message()

    def test_checkout_requires_postal_code(self, driver, logged_in_inventory):
        logged_in_inventory.add_product_to_cart("Sauce Labs Backpack")
        logged_in_inventory.open_cart()
        CartPage(driver).proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_information("João", "Silva", "")
        assert "Postal Code is required" in checkout.get_error_message()


@pytest.mark.e2e
@pytest.mark.smoke
class TestEndToEndPurchase:
    """Fluxo ponta a ponta: login -> adicionar produtos -> checkout -> finalizar."""

    def test_complete_purchase_flow_single_product(self, driver):
        LoginPage(driver).load().login(
            USERS["standard"]["username"], USERS["standard"]["password"]
        )

        inventory = InventoryPage(driver)
        assert inventory.is_loaded()
        inventory.add_product_to_cart("Sauce Labs Backpack")
        assert inventory.get_cart_badge_count() == 1
        inventory.open_cart()

        cart = CartPage(driver)
        assert cart.get_items_count() == 1
        assert "Sauce Labs Backpack" in cart.get_item_names()
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_information(
            CHECKOUT_INFO["first_name"],
            CHECKOUT_INFO["last_name"],
            CHECKOUT_INFO["postal_code"],
        )

        assert checkout.get_items_in_summary() == 1
        subtotal = checkout.get_subtotal()
        total = checkout.get_total()
        assert subtotal > 0
        assert total >= subtotal

        checkout.finish_purchase()

        assert checkout.is_purchase_complete()
        assert "Thank you for your order" in checkout.get_completion_message()

    def test_complete_purchase_flow_multiple_products(self, driver):
        LoginPage(driver).load().login(
            USERS["standard"]["username"], USERS["standard"]["password"]
        )

        inventory = InventoryPage(driver)
        products = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        for product in products:
            inventory.add_product_to_cart(product)

        assert inventory.get_cart_badge_count() == len(products)
        inventory.open_cart()

        cart = CartPage(driver)
        assert cart.get_items_count() == len(products)
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_information(
            CHECKOUT_INFO["first_name"],
            CHECKOUT_INFO["last_name"],
            CHECKOUT_INFO["postal_code"],
        )

        assert checkout.get_items_in_summary() == len(products)
        checkout.finish_purchase()

        assert checkout.is_purchase_complete()
        completion_msg = checkout.get_completion_message()
        assert "Thank you for your order" in completion_msg
