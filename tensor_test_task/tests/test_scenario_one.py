from pages.sbis_page import SbisPage
from pages.tensor_page import TensorPage


def test_first_scenario(browser):
    sbis_page = SbisPage(browser)
    tensor_page = TensorPage(browser)

    # Step 1-3: Переход в раздел «Контакты», нажатие по баннеру «Тензор» и переход на сайт «tensor.ru»
    sbis_page.open('https://sbis.ru/')
    sbis_page.click_contacts()
    sbis_page.click_tensor_banner()

    # Step 4: Проверка блока «Сила в людях» на сайте «tensor.ru»
    assert tensor_page.is_people_power_block_present(), 'Блок «Сила в людях» не найден'

    # Step 5: Кликаем на «Подробнее» и проверяем URL
    tensor_page.click_more_link()
    assert 'tensor.ru/about' in browser.current_url, 'Не удалось перейти на страницу «О компании»'

    # Step 6: Проверка размеров изображений в разделе «Работаем»
    assert tensor_page.check_image_dimensions(), 'Изображения имеют разные размеры'
