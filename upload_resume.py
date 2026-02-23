from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.naukri.com/nlogin/login")

        wait = WebDriverWait(driver, 20)

        # Wait for email field
        email_field = wait.until(
            EC.presence_of_element_located((By.ID, "usernameField"))
        )

        time.sleep(random.randint(2, 4))

        email_field.send_keys(os.environ["NAUKRI_EMAIL"])

        password_field = driver.find_element(By.ID, "passwordField")
        password_field.send_keys(os.environ["NAUKRI_PASSWORD"])
        password_field.send_keys(Keys.RETURN)

        # Wait after login
        time.sleep(random.randint(5, 8))

        driver.get("https://www.naukri.com/mnjuser/profile")

        # Wait for upload input
        upload_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )

        time.sleep(random.randint(3, 5))

        upload_input.send_keys("Niveditha_P-Resume.pdf")

        time.sleep(5)

        driver.quit()
        return True

    except Exception as e:
        print("Error:", e)
        driver.quit()
        return False


# Retry logic
success = False

for attempt in range(2):
    success = upload_resume()
    if success:
        print("Resume uploaded successfully!")
        send_email(
            "Naukri Resume Upload Successful",
            "Your automated resume upload completed successfully."
        )
        break
    else:
        time.sleep(10)

if not success:
    send_email(
        "Naukri Resume Upload Failed",
        "The automated resume upload failed. Please check GitHub Actions logs."
    )
