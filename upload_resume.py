from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
import random
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body):
    sender = os.environ["ALERT_EMAIL"]
    password = os.environ["ALERT_PASSWORD"]
    receiver = os.environ["ALERT_EMAIL"]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

def upload_resume():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(random.randint(3, 6))

        driver.find_element(By.ID, "usernameField").send_keys(os.environ["nivedithap118@gmail.com"])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ["nivedithap@11898"])
        driver.find_element(By.ID, "passwordField").send_keys(Keys.RETURN)

        time.sleep(random.randint(5, 8))

        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(random.randint(5, 8))

        upload = driver.find_element(By.XPATH, "//input[@type='file']")
        upload.send_keys("Niveditha_P-Resume.pdf")

        time.sleep(5)

        driver.quit()
        return True

    except Exception as e:
        driver.quit()
        print("Error:", e)
        return False

# Retry logic
for attempt in range(2):
    success = upload_resume()
    if success:
        print("Resume uploaded successfully!")
        break
    else:
        time.sleep(10)

if not success:
    send_email(
        "Naukri Resume Upload Failed",
        "The automated resume upload failed. Please check GitHub Actions logs."
    )
