import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

# Test credentials and URLs
ADMIN_EMAIL = "admin@mail.fr"
ADMIN_PASSWORD = "password1"
LOGIN_URL = "http://localhost:3000/admin/login"
PRODUCTS_URL = "http://localhost:3000/admin/products/new"

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_driver(driver):
    """Fixture to handle login before product creation test"""
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
    
    # Wait for dashboard heading to confirm login success
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title"))
        )
    except TimeoutException:
        pytest.fail("Login failed - Dashboard not found")
    
    return driver

def test_create_product(logged_in_driver):
    """Test complete product creation process"""
    driver = logged_in_driver
    
    # Navigate directly to new product page
    driver.get("http://localhost:3000/admin/products/new")
    
    # Wait for the product form to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "name"))
    )
    
    # Fill in general product information
    name_input = driver.find_element(By.ID, "name")
    sku_input = driver.find_element(By.ID, "sku")
    price_input = driver.find_element(By.ID, "price")
    weight_input = driver.find_element(By.ID, "weight")
    
    name_input.send_keys("T-shirt Noir")
    sku_input.send_keys("TSH-001")
    price_input.send_keys("19.99")
    weight_input.send_keys("0.5")
    
    # Select category
    select_category_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.text-interactive"))
    )
    select_category_link.click()
    
    # Wait for category selection modal and select Men category
    men_select_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h3[contains(., 'Men')]/following::button[1]"))
    )
    men_select_button.click()
    
    # Click on description editor icon first
    description_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#'] svg[width='48']"))
    )
    description_icon.click()
    
    # Then wait for and fill the description editor
    description_editor = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ce-paragraph[contenteditable='true']"))
    )
    description_editor.click()
    description_editor.send_keys("Un t-shirt noir basique")
    
    # Upload image
    image_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "label[for^='mbr'] svg[viewBox='0 0 20 20']"))
    )
    image_input.click()
    # Get the absolute path of the image
    image_path = os.path.abspath("./img/TSnoir.jpg")
    # Find the actual file input element that is hidden
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(image_path)
    
    # Fill in SEO information
    url_key_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "urlKey"))
    )
    meta_title_input = driver.find_element(By.ID, "metaTitle")
    meta_keywords_input = driver.find_element(By.ID, "metaKeywords")
    meta_description_input = driver.find_element(By.ID, "meta_description")
    
    url_key_input.send_keys("tshirt-noir")
    meta_title_input.send_keys("tshirt-noir")
    meta_keywords_input.send_keys("tshirt-noir")
    meta_description_input.send_keys("tshirt-noir")
    
    # Set quantity
    qty_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "qty"))
    )
    qty_input.clear()
    qty_input.send_keys("100")
    
    # Select attributes
    color_select = Select(driver.find_element(By.ID, "attributes[0][value]"))
    color_select.select_by_value("2")  # Black
    
    size_select = Select(driver.find_element(By.ID, "attributes[1][value]"))
    size_select.select_by_value("5")  # XL
    
    # Save the product
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary"))
    )
    save_button.click()
    
    # Wait for success message
    try:
        success_toast = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.Toastify__toast--success"))
        )
        assert "Product saved successfully!" in success_toast.text
    except TimeoutException:
        pytest.fail("Product save confirmation not found")
    
    # Verify all fields were saved correctly
    assert name_input.get_attribute("value") == "T-shirt Noir"
    assert sku_input.get_attribute("value") == "TSH-001"
    assert price_input.get_attribute("value") == "19.99"
    assert weight_input.get_attribute("value") == "0.5"
    assert url_key_input.get_attribute("value") == "tshirt-noir"
    assert meta_title_input.get_attribute("value") == "tshirt-noir"
    assert meta_keywords_input.get_attribute("value") == "tshirt-noir"
    assert meta_description_input.get_attribute("value") == "tshirt-noir"
    assert qty_input.get_attribute("value") == "100"
    assert color_select.first_selected_option.get_attribute("value") == "2"
    assert size_select.first_selected_option.get_attribute("value") == "5"
