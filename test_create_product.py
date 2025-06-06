import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



@pytest.fixture
def driver():
    options = Options()
    # options.add_argument('--headless')  # Enlevez cette ligne pour voir le navigateur
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
import time
from selenium.webdriver.common.by import By

def admin_login(driver):
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

def test_create_product(driver):

    # Attendre que le lien soit cliquable, puis cliquer
    new_product_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(By.CSS_SELECTOR, "a[href='/admin/products/new']")
    )
    new_product_link.click()

    # 3. Vérification que l'on est bien sur la page "Create a new product"
    assert "products/new" in driver.current_url
    assert "Create a new product" in driver.page_source

    # 4. Remplir le champ "Name" (champ id="name")
    name_input = driver.find_element(By.ID, "name")
    name_input.send_keys("Test Product Selenium")

    # 5. Soumettre le formulaire
    product_form = driver.find_element(By.ID, "productForm")
    product_form.submit()

    # 7. Vérification que le produit a été ajouté (redirection, alerte, ou retour à la liste, selon implémentation)
    assert "products" in driver.current_url
    assert "Test Product Selenium" in driver.page_source  # si le nom apparaît

