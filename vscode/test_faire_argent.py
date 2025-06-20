from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as chromeservice
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import time

driver= webdriver.Chrome(service=chromeservice(ChromeDriverManager().install()))

driver.get( "http://localhost:3000/classic-leather-loafers" )



driver.find_element(By.CSS_SELECTOR, ".button.primary.outline").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, ".add-cart-popup-button").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, ".shopping-cart-checkout-btn.flex.justify-between.mt-8").find_element(By.CSS_SELECTOR, ".button.primary").click()
driver.find_element(By.NAME, "email" ).send_keys("client@mail.fr")
driver.find_element(By.CSS_SELECTOR, ".button.primary").click()
WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".checkout-payment.checkout-step"))
    )

# on rempli le form de shipping
driver.find_element(By.NAME, "address[full_name]").send_keys("Nom prenom")
driver.find_element(By.NAME, "address[telephone]").send_keys("0607080911")
driver.find_element(By.NAME, "address[address_1]").send_keys("rue des fruits")
driver.find_element(By.NAME, "address[city]").send_keys("Charbo")
driver.find_element(By.NAME, "address[postcode]").send_keys("69999")
driver.find_element(By.NAME, "address[telephone]").send_keys("0607080911")
Select(driver.find_element(By.ID, "address[country]")).select_by_index(1)
Select(driver.find_element(By.ID, "address[province]")).select_by_index(1)
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "label[for='method0']"))).click()
driver.find_element(By.CSS_SELECTOR, "button[type='submit'].primary").click()
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.flex.justify-start.items-center.gap-4 a"))
).click()
# Attendre que l’iframe Stripe soit là
iframe = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[name^='__privateStripeFrame']"))
)

# on passe dans l’iframe
driver.switch_to.frame(iframe)

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "number"))  # parfois "number" selon le nom attribué
)

# Remplir la carte
driver.find_element(By.NAME, "number").send_keys("4242424242424242")
driver.find_element(By.NAME, "expiry").send_keys("0426")
driver.find_element(By.NAME, "cvc").send_keys("242")

# on ressort de l'iframe
driver.switch_to.default_content()

#on fait l'argent
driver.find_element(By.CSS_SELECTOR, ".form-submit-button").find_element(By.CSS_SELECTOR, ".button.primary").click()
time.sleep(12)

#faut verifier l'argent