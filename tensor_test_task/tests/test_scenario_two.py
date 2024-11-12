from pages.sbis_page import SbisPage


def test_second_scenario(browser):
    sbis_page = SbisPage(browser)

    # Step 1: Переход в раздел «Контакты»
    sbis_page.open('https://sbis.ru/')
    sbis_page.click_contacts()

    # Step 2: Проверка региона и первого партнера из списка партнеров
    assert 'Тюменская обл.' in sbis_page.get_region(), 'Регион по умолчанию неверный'
    assert 'СБИС - Тюмень' in sbis_page.get_partner(), 'Первый партнёр из списка неверный'

    # Step 3: Смена региона на Камчатский край и проверка изменений
    sbis_page.change_region()

    # Step 4: Проверка изменений после смены региона
    assert 'Камчатский край' in sbis_page.get_region(), 'Регион не изменился на «Камчатский край»'
    assert 'СБИС - Камчатка' in sbis_page.get_partner(), 'Список партнеров не изменился на «Камчатский край»'
    assert '41-kamchatskij-kraj' in browser.current_url, 'URL не содержит новый регион'
