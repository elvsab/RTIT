import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.fixture()
def driver():
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service)
    driver.maximize_window()
    driver.get('https://b2c.passport.rt.ru/auth')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located([By.CLASS_NAME, "tabs-input-container"])
    )
    yield driver
    driver.quit()
