from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from .base_page import BasePage, logger


class TensorPage(BasePage):
    PEOPLE_POWER_BLOCK = (
        By.XPATH, "//p[contains(@class, 'tensor_ru-Index__card-title') and text()='Сила в людях']"
    )
    MORE_LINK = (
        By.XPATH, "//a[contains(@class, 'tensor_ru-link tensor_ru-Index__link') and "
                  "text()='Подробнее' and @href='/about']"
    )
    WORK_SECTION_IMAGES = (By.XPATH, "//img[contains(@class, 'tensor_ru-About__block3-image')]")

    def is_people_power_block_present(self):
        """Проверяет наличие блока «Сила в людях» на странице."""
        block_name = 'Сила в людях'
        logger.info(f'Проверка наличия блока "{block_name}"')
        try:
            logger.debug(f'Проверка наличия блока "{block_name}" в элементе {self.PEOPLE_POWER_BLOCK}')
            element = self.find_element(self.PEOPLE_POWER_BLOCK)
            if block_name in element.text:
                logger.info(f'Блок "{block_name}" присутствует в элементе {self.PEOPLE_POWER_BLOCK}')
                return True
            else:
                logger.warning(f'Блок "{block_name}" не найден в элементе {self.PEOPLE_POWER_BLOCK}')
                return False
        except NoSuchElementException:
            logger.error(f'Элемент с локатором {self.PEOPLE_POWER_BLOCK} не '
                         f'найден для проверки блока "{block_name}"')
            return False

    def click_more_link(self):
        """Кликает на ссылку «Подробнее» в блоке «Сила в людях», чтобы перейти на страницу «О компании»."""
        logger.info('Переход в раздел "Подробнее"')
        self.click_element(self.MORE_LINK)
        logger.info('Выполнен переход в раздел "Подробнее"')

    def check_image_dimensions(self):
        """Проверяет, что все изображения в разделе «Работаем» имеют одинаковый размер."""
        logger.info('Проверка размеров изображений в разделе "Работаем"')
        images = self.browser.find_elements(*self.WORK_SECTION_IMAGES)
        if not images:
            logger.warning('Изображения не найдены в разделе "Работаем"')
            return False

        sizes = [(img.size['height'], img.size['width']) for img in images]
        first_size = sizes[0]
        all_same_size = all(size == first_size for size in sizes)

        if all_same_size:
            logger.info('Все изображения имеют одинаковый размер')
        else:
            logger.warning('Обнаружены изображения с различными размерами')

        return all_same_size
