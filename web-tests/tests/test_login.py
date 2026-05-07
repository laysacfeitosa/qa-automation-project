import pytest
from utils.config import USERS
from pages.inventory_page import InventoryPage


@pytest.mark.login
@pytest.mark.smoke
class TestLogin:

    def test_login_with_valid_credentials(self, driver, login_page):
        login_page.login(USERS["standard"]["username"], USERS["standard"]["password"])

        inventory = InventoryPage(driver)
        assert inventory.is_loaded()
        assert "inventory.html" in inventory.current_url()

    def test_login_with_locked_user_shows_error(self, login_page):
        login_page.login(USERS["locked"]["username"], USERS["locked"]["password"])

        assert login_page.has_error()
        assert "locked out" in login_page.get_error_message().lower()

    def test_login_with_invalid_password_shows_error(self, login_page):
        login_page.login(USERS["standard"]["username"], "senha_errada")

        assert login_page.has_error()
        assert "username and password" in login_page.get_error_message().lower()

    def test_login_with_empty_fields_shows_error(self, login_page):
        login_page.login("", "")

        assert login_page.has_error()
        assert "required" in login_page.get_error_message().lower()
