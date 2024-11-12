import logging

import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def browser():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    browser = webdriver.Firefox(options=options)
    yield browser
    browser.quit()


def setup_logger():
    """Настройки логирования."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s, %(filename)s, %(funcName)s')

    # FileHandler для записи всех логов в файл
    file_handler = logging.FileHandler('main.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # StreamHandler для вывода логов уровня INFO и выше в терминал
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
