import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import valid_email, valid_password, base_url


@pytest.fixture(autouse=True)
def test_driver():
    driver = webdriver.Chrome('C:/Users/Flame/PycharmProjects/chromedriver.exe')
    driver.implicitly_wait(5)
    driver.get(f'{base_url}login')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'email'))).send_keys(valid_email)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'pass'))).send_keys(valid_password)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    assert driver.find_element(By.TAG_NAME, 'h1').text == 'PetFriends'

    yield

    driver.quit()


# явные ожидания, проверка карточек питомцев

def test_web_driver_wait(test_driver):
    images = WebDriverWait(test_driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-img-top'))
    )
    names = WebDriverWait(test_driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-body .card-title'))
    )
    descriptions = WebDriverWait(test_driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-body .card-text'))
    )

    src_images = [i.get_attribute('src') for i in images]
    text_names = [i.text for i in names]
    text_ages = [i.text.split(', ')[1] for i in descriptions]

    assert len(src_images) == len(text_names)
    assert len(src_images) == len(text_ages)


# неявные ожидания, проверка таблицы питомцев

def test_implicitly_wait(test_driver):
    test_driver.implicitly_wait(5)

    test_driver.get(f'{base_url}my_pets')

    images = test_driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/th[1]')
    names = test_driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/td[2]')
    ages = test_driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/td[3]')

    src_images = [i.get_attribute('src') for i in images]
    text_names = [i.text for i in names]
    text_ages = [i.text for i in ages]

    assert len(src_images) == len(text_names)
    assert len(src_images) == len(text_ages)
