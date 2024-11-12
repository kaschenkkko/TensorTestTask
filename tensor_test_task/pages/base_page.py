import pytest
from conftest import setup_logger
from selenium.common.exceptions import (TimeoutException,
                                        UnexpectedAlertPresentException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = setup_logger()


class BasePage:
    def __init__(self, browser):
        self.browser = browser

    def open(self, url):
        """Открывает веб-страницу по указанному URL."""
        logger.info(f'Открытие страницы {url}')
        self.browser.get(url)

    def find_element(self, locator, timeout=10):
        """Находит элемент на странице по указанному локатору."""
        try:
            logger.debug(f'Поиск элемента с локатором {locator}')
            element = WebDriverWait(self.browser, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.info(f'Элемент найден: {locator}')
            return element
        except TimeoutException:
            error_message = f'Элемент с локатором {locator} не найден после {timeout} секунд ожидания'
            logger.error(error_message)
            pytest.fail(error_message)
        except UnexpectedAlertPresentException:
            alert = self.browser.switch_to.alert
            message = f'Текст всплывающего окна: {alert.text}'
            logger.error(message)
            pytest.fail(message)

    def wait_for_no_overlay(self):
        """Ожидает исчезновения overlay-элемента."""
        logger.debug('Ожидание исчезновения overlay')
        WebDriverWait(self.browser, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[name='loadingOverlay']"))
        )

    def click_element(self, locator, timeout=10):
        """Кликает на элемент."""
        logger.debug(f'Клик на элемент с локатором {locator}')
        self.wait_for_no_overlay()
        element = self.find_element(locator, timeout)
        element.click()
        logger.info(f'Выполнен клик по элементу: {locator}')
