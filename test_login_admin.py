# le jeux de clés est :
# email : admin@mail.fr
# password : password1

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Test credentials
ADMIN_EMAIL = "admin@mail.fr"
ADMIN_PASSWORD = "password1"
LOGIN_URL = "http://localhost:3000/admin/login"

@pytest.fixture
def driver():
    # Setup Chrome driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_login_success(driver):
    """Test successful admin login"""
    driver.get(LOGIN_URL)
    
    # Wait for and fill in login form
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    password_input = driver.find_element(By.NAME, "password")
    
    email_input.send_keys(ADMIN_EMAIL)
    password_input.send_keys(ADMIN_PASSWORD)
    
    # Click login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    
    # Wait for dashboard heading
    try:
        dashboard_heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title"))
        )
        assert dashboard_heading.text == "Dashboard"
    except TimeoutException:
        pytest.fail("Dashboard heading not found after login")

def test_login_invalid_credentials(driver):
    """Test login with invalid credentials"""
    driver.get(LOGIN_URL)
    
    # Wait for and fill in login form with wrong password
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    password_input = driver.find_element(By.NAME, "password")
    
    email_input.send_keys(ADMIN_EMAIL)
    password_input.send_keys("wrongpassword")
    
    # Click login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    
    # Wait for error message
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.text-critical"))
        )
        assert error_message.text == "Invalid email or password"
    except TimeoutException:
        pytest.fail("Error message not found after invalid login attempt")

def test_login_invalid_email_format(driver):
    """Test login with invalid email format"""
    driver.get(LOGIN_URL)
    
    # Wait for and fill in login form with invalid email
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    password_input = driver.find_element(By.NAME, "password")
    
    email_input.send_keys("invalidemail")
    password_input.send_keys(ADMIN_PASSWORD)
    
    # Click login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    
    # Wait for email format error message
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.pl025.text-critical"))
        )
        assert error_message.text == "Invalid email"
    except TimeoutException:
        pytest.fail("Email format error message not found")









