import psutil
import os
import sys

os.system("pkill -9 chrome")
def kill_chrome():
    for process in psutil.process_iter(attrs=["pid", "name"]):
        if "chrome" in process.info["name"].lower():
            try:
                p = psutil.Process(process.info["pid"])
                p.terminate()
            except psutil.NoSuchProcess:
                pass

kill_chrome()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

options = Options()
USER_DATA_DIR = "/tmp/seedloaf-session"
options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
options.add_argument("--profile-directory=Default")
options.binary_location = "/opt/chrome/chrome"
options.add_argument("--headless=new")
options.add_argument("window-size=1920x1080")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--enable-javascript")
options.add_argument("--disable-web-security")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-features=IsolateOrigins,site-per-process")
options.add_argument("--disable-extensions")

service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(options=options, service=service)

try:
    driver.get("https://accounts.seedloaf.com/sign-in")
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script("return document.readyState") == "complete")

    usernamesec = os.getenv("SEEDLOAF_EMAIL")
    passwordsec = os.getenv("SEEDLOAF_PASSWORD")

    try:
        WebDriverWait(driver, 10).until(lambda d: "dashboard" in d.current_url)
        print("✅ Already logged in")
    except:
        print("🔐 Logging in...")

        username = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "identifier-field"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", username)
        driver.execute_script("arguments[0].click();", username)
        username.send_keys(usernamesec)
        username.send_keys(Keys.RETURN)
        time.sleep(5)

        try:
            error_elem = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.ID, "error-identifier"))
            )
            if error_elem:
                print("Username is incorrect")
                driver.quit()
                sys.exit()
        except:
            pass

        password = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "password-field"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", password)
        driver.execute_script("arguments[0].click();", password)
        password.send_keys(passwordsec)
        password.send_keys(Keys.RETURN)
        time.sleep(8)
        print("entered password")

    # Click Stop button
    try:
        wait = WebDriverWait(driver, 20)
        stopworld = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-error')]")))
        print("Stop button found")

        driver.execute_script("arguments[0].scrollIntoView(true);", stopworld)
        driver.execute_script("arguments[0].click();", stopworld)
        print("Clicked stop")
        time.sleep(2)

    except:
        try:
            startworld = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "button.btn-primary"))
            )
            print("Start button found — world already stopped.")
        except:
            print("Neither Start nor Stop button found.")

finally:
    driver.quit()
