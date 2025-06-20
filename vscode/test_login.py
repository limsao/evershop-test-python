from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as chromeservice
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import os
import time

def test_login():


    
    options = webdriver.ChromeOptions()
    # Désactive les popups, notifications, géolocalisation, etc.
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.geolocation": 2,
        "profile.default_content_setting_values.popups": 2
    }
    options.add_argument("--incognito")
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")

    driver= webdriver.Chrome(options=options, service=chromeservice(ChromeDriverManager().install()))

    driver.get( "http://localhost:3000/admin/login" )

    driver.find_element(By.NAME, "email" ).send_keys("admin@mail.fr")
    driver.find_element(By.NAME, "password").send_keys("password1")

    driver.find_element(By.CSS_SELECTOR, ".form-submit-button").find_element(By.CSS_SELECTOR, ".button").click()


    #creation de categorie
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex.justify-left"))
    )
    driver.find_elements(By.CSS_SELECTOR, ".flex.justify-left" )[4] .click()

    driver.find_element(By.CSS_SELECTOR, ".button.primary").click()

    driver.find_element(By.CSS_SELECTOR, "#name").send_keys("homme")
    driver.find_element(By.CSS_SELECTOR, "#urlKey").send_keys("homme")

    driver.find_element(By.CSS_SELECTOR, ".button.primary").click()

    #creation de produit
    driver.find_elements(By.CSS_SELECTOR, ".flex.justify-left" )[1] .click()

    driver.find_element(By.CSS_SELECTOR, "#name").send_keys("T-shirt Été")
    driver.find_element(By.CSS_SELECTOR, "#sku").send_keys("PROD-ETE-001")
    driver.find_element(By.CSS_SELECTOR, "#price").send_keys("19")
    driver.find_element(By.CSS_SELECTOR, "#weight").send_keys("1")

    driver.find_element(By.CSS_SELECTOR, ".text-interactive").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay.fadeIn"))
    )
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search categories"]').send_keys("homme")
    driver.find_element(By.CSS_SELECTOR, ".button.secondary").click()
    

    driver.find_element(By.CSS_SELECTOR, "#tax_class").click()
    Select(driver.find_element(By.ID, "tax_class")).select_by_index(0) #je choisie la valeur 0 soit none du menu deroulant.
    driver.find_element(By.CSS_SELECTOR, ".editor.form-field-container").find_elements(By.CSS_SELECTOR, 'a[href="#"]')[0].click()

    driver.find_element(By.CSS_SELECTOR, "div.ce-paragraph[contenteditable='true']").send_keys("description du produit")
    driver.find_element(By.CSS_SELECTOR, ".uploader-icon").find_element(By.CSS_SELECTOR, 'svg.h-5.w-5').click()

    driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(os.path.abspath("./img/TSnoir.jpg"))

    driver.find_element(By.ID, "urlKey").send_keys("t-shirt-ete")
    driver.find_element(By.ID, "metaTitle").send_keys("T-shirt Été")
    driver.find_element(By.ID, "metaKeywords").send_keys("t-shirt, été, vêtements")
    driver.find_element(By.ID, "meta_description").send_keys("Découvrez notre t-shirt idéal pour la saison estivale.")

    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'label[for="status1"]')).click().perform()
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'label[for="visibility1"]')).click().perform()
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'label[for="manage_stock1"]')).click().perform()
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'label[for="stock_availability1"]')).click().perform()
    driver.find_element(By.ID, "qty").send_keys("100")

    Select(driver.find_element(By.ID, "attributes[0][value]")).select_by_value("2")
    Select(driver.find_element(By.ID, "attributes[1][value]")).select_by_value("5")

    driver.find_element(By.CSS_SELECTOR, ".button.primary").click()
    
    # quelques assert histoire de verifier que c bien rempli( à compléter )

    assert EC.presence_of_element_located((By.CSS_SELECTOR, "div.Toastify__toast--success"))
    assert driver.find_element(By.CSS_SELECTOR, "#name").get_attribute("value") == "T-shirt Été"
    assert driver.find_element(By.CSS_SELECTOR, "#sku"). get_attribute("value") == "PROD-ETE-001"
    assert driver.find_element(By.CSS_SELECTOR, "#price").get_attribute("value") == "19"
    assert driver.find_element(By.CSS_SELECTOR, "#weight").get_attribute("value") == "1"
    assert driver.find_element(By.CSS_SELECTOR, ".text-gray-500").text == "homme"
    

    #suppression du produit

    driver.find_elements(By.CSS_SELECTOR, ".flex.justify-left" )[3] .click() # bouton categories

    rows = driver.find_elements(By.CSS_SELECTOR, "table.listing tbody tr")

    for row in rows:
        # Chercher la cellule contenant le SKU
        cells = row.find_elements(By.CSS_SELECTOR, "td")
        if not cells:
            continue  # ligne vide

        sku_text = cells[4].text.strip()  # 5ème colonne = SKU

        if sku_text == "PROD-ETE-001":
            # La checkbox est dans la première cellule (td)
            checkbox_label = cells[0].find_element(By.TAG_NAME, "label")
            checkbox_label.click()
            break

    driver.find_element(By.LINK_TEXT, "Delete").click()
    
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay.fadeIn"))
    )
    driver.find_element(By.CSS_SELECTOR, ".button.critical").click()
    
    time.sleep(1)
    assert "PROD-ETE-001" not in (driver.find_element(By.CSS_SELECTOR, "table.listing")).text


    


