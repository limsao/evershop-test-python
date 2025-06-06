import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_admin_login(driver):
    driver.get("http://localhost:3000/admin/login")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    ).send_keys("admin@mail.fr")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    ).send_keys("password1")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary"))
    ).click()

    # Vérifie que la navigation admin est présente
    nav = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "admin-navigation"))
    )

    assert nav is not None

