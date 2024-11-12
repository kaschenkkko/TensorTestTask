from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage, logger


class SbisPage(BasePage):
    CONTACTS_LINK = (
        By.XPATH, "//div[contains(@class, 'sbisru-Footer')]//a[contains(@class, 'sbisru-Footer__link') and "
                  "contains(text(), 'Контакты')]"
    )
    TENSOR_BANNER = (
        By.XPATH, "//a[contains(@class, 'sbisru-Contacts__logo-tensor') and "
                  "contains(@title, 'tensor.ru')]"
    )
    SBIS_REGION = (By.XPATH, "//span[contains(@class, 'sbis_ru-Region-Chooser')]")
    SBIS_PARTNER = (By.XPATH, "(//div[contains(@class, 'sbisru-Contacts-List__name')])")

    def click_contacts(self):
        """Переходит к разделу «Контакты» на странице, кликая по соответствующей ссылке."""
        logger.info('Переход к разделу "Контакты"')
        self.click_element(self.CONTACTS_LINK)
        logger.info('Выполнен переход к разделу "Контакты"')

    def click_tensor_banner(self):
        """Кликает на баннер «Тензор» на странице «Контакты» и переключается на новую вкладку."""
        logger.info('Переход на сайт "tensor.ru" через клик по баннеру')

        self.click_element(self.TENSOR_BANNER)
        self.browser.switch_to.window(self.browser.window_handles[-1])

        logger.info('Выполнен переход на сайт "tensor.ru", в новой вкладке')

    def get_region(self):
        """Получает текущий регион."""
        logger.info('Получение региона')
        region_element = self.find_element(self.SBIS_REGION)
        logger.info(f'Получен регион {region_element.text}')

        return region_element.text

    def get_partner(self):
        """Получает первого партнера с текущей страницы, не учитывая скрытые или невидимые элементы."""
        logger.info('Получение первого партнера из списка')
        visible_partner_elements = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_all_elements_located(self.SBIS_PARTNER)
        )
        logger.info(f'Получен первый партнер из списка {visible_partner_elements[0].text}')

        return visible_partner_elements[0].text

    def change_region(self, region_name='Камчатский край'):
        """Изменяем регион на необходимый, на сайте «sbis.ru/contacts»."""
        logger.info('Открытие панели выбора региона')
        self.click_element(self.SBIS_REGION)

        # Ожидание открытия панели
        region_list_locator = (By.XPATH, "//div[contains(@class, 'sbis_ru-Region-Panel')]")
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(region_list_locator)
        )
        logger.info('Панель выбора региона загружена и готова к взаимодействию')

        logger.debug('Выбор необходимого региона')
        new_region_locator = (
            By.XPATH, "//li[contains(@class, 'sbis_ru-Region-Panel__item')]"
                      f"//span[contains(@title, '{region_name}')]"
        )
        # Без двойного клика возникает ошибка
        self.click_element((By.XPATH, "//h5[contains(@class, 'sbisru-h5 sbis_ru-Region-Panel')]"))
        self.click_element(new_region_locator)

        logger.debug(f'Ожидание обновления региона на "{region_name}"')
        current_region_locator = (
            By.XPATH, f"//span[contains(@class, 'sbis_ru-Region-Chooser__text') and text()='{region_name}']"
        )
        WebDriverWait(self.browser, 20).until(
            EC.text_to_be_present_in_element(current_region_locator, region_name)
        )

        logger.info(f'Регион успешно изменён на "{region_name}"')
