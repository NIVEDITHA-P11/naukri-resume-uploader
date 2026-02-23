from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.naukri.com/nlogin/login")
    time.sleep(3)

    driver.find_element(By.ID, "usernameField").send_keys(os.environ["nivedithap118@gmail.com"])
    driver.find_element(By.ID, "passwordField").send_keys(os.environ["nivedithap@11898"])
    driver.find_element(By.ID, "passwordField").send_keys(Keys.RETURN)

    time.sleep(5)

    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(5)

    upload = driver.find_element(By.XPATH, "//input[@type='file']")
    upload.send_keys("Niveditha_P-Resume.pdf")

    time.sleep(5)

    print("Resume uploaded successfully!")

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()