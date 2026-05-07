import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import pytest
from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import USERS

SCREENSHOTS_DIR = Path(__file__).parent.parent / "reports" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture
def driver():
    drv = DriverFactory.get_chrome_driver()
    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver):
    return LoginPage(driver).load()


@pytest.fixture
def logged_in_inventory(driver):
    """Atalho: faz login com usuário standard e devolve a página de inventário."""
    LoginPage(driver).load().login(
        USERS["standard"]["username"], USERS["standard"]["password"]
    )
    inv = InventoryPage(driver)
    assert inv.is_loaded(), "Inventário não carregou após login"
    return inv


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Salva screenshot quando o teste falha."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            filename = f"{item.name}.png"
            path = SCREENSHOTS_DIR / filename
            try:
                driver.save_screenshot(str(path))
                print(f"\n[Screenshot salvo] {path}")
            except Exception as e:
                print(f"\n[Erro ao salvar screenshot] {e}")
