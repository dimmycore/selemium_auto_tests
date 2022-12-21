import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import valid_email, valid_password, base_url


@pytest.fixture(autouse=True)
def test_driver():
    driver = webdriver.Chrome('C:/Users/Flame/PycharmProjects/chromedriver.exe')
    driver.get(f'{base_url}login')

    email_input = driver.find_element(By.CSS_SELECTOR, 'input#email')
    email_input.clear()
    email_input.send_keys(valid_email)

    pass_input = driver.find_element(By.CSS_SELECTOR, 'input#pass')
    pass_input.clear()
    pass_input.send_keys(valid_password)

    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    assert driver.find_element(By.TAG_NAME, 'h1').text == 'PetFriends'

    yield

    driver.quit()

# тесты которые проверяют что на странице со списком питомцев пользователя:


# 1. присутствуют все питомцы
def test_check_my_pet(test_driver):
    pet_tag = test_driver.find_element(By.XPATH, "//div[contains(@class,'task3')]/div[1]")
    pet_count = int(pet_tag.text.split('\n')[1].split(':')[1])
    pet_rows = test_driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr")
    assert pet_count == len(pet_rows)


# 2. хотя бы у половины питомцев есть фото
def test_check_half_pets_have_photo(test_driver):
    pet_images = test_driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr/th/img")
    count = 0
    for i in range(len(pet_images)):
        if pet_images[i].get_attribute('src') != 'unknown':
            count += 1
    assert count >= len(pet_images) / 2


# у всех питомцев есть имя, возраст и порода
def test_pet_has_name_age_kind(test_driver):
    pet_data_complete = test_driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr/td")
    for pet_data in pet_data_complete:
        assert pet_data.text.strip() != ''


# у всех питомцев разные имена
def test_all_names_are_different(test_driver):
    pets_names = test_driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr/td[1]")
    list_names = []
    for pets_names in pets_names:
        list_names.append(pets_names.text)
    assert len(list_names) == len(set(list_names))


# в списке нет повторяющихся питомцев
def test_all_pets_are_different(test_driver):
    all_pets = test_driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr")
    list_pets = []

    for all_pets in all_pets:
        list_pets.append(all_pets.text)
    assert len(set(list_pets)) == len(list_pets)
