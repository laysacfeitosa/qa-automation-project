from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from utils.config import HEADLESS


class DriverFactory:
    """Centraliza a criação do WebDriver para reuso em fixtures e CI."""

    @staticmethod
    def get_chrome_driver() -> webdriver.Chrome:
        options = Options()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(5)
        return driver
