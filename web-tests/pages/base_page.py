from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.config import DEFAULT_TIMEOUT


class BasePage:
    """Métodos genéricos compartilhados por todas as páginas (Page Object base)."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    def open(self, url: str):
        self.driver.get(url)

    def find(self, locator: tuple[str, str]):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator: tuple[str, str]):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator: tuple[str, str], text: str):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple[str, str]) -> str:
        return self.find(locator).text

    def is_visible(self, locator: tuple[str, str]) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def is_present(self, locator: tuple[str, str]) -> bool:
        return len(self.driver.find_elements(*locator)) > 0

    def find_all(self, locator: tuple[str, str]):
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def current_url(self) -> str:
        return self.driver.current_url