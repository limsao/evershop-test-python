# Voici un config pour ouvrir le navigateur pour mes tests selenium
# Configuration pour les tests admin
ADMIN_LOGIN_URL = "http://localhost:3000/admin"
ADMIN_EMAIL = "admin@mail.fr"
ADMIN_PASSWORD = "password1"
from selenium import webdriver

def get_driver():
    """Ouvre et retourne une instance du navigateur Chrome pour les tests Selenium."""
    driver = webdriver.Chrome()
    return driver