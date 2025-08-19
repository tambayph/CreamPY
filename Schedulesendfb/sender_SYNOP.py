from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timezone

# === Input Section ===
date_str = input("Enter the date (YYYY-MM-DD): ")
time_str = input("Enter the time (HH:MM, UTC format): ")
SYNOP = input("Enter the SYNOP: ")
rainfall = input("Enter the rainfall value (in mm): ")

utz = time_str.replace(":", "")
message_SYNOP = f"{SYNOP}"
message_RR = f"ROXAS {utz}Z RR={rainfall} mm"

# === Calculate Scheduled UTC Time ===
scheduled_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
now_utc = datetime.now(timezone.utc)

if now_utc >= scheduled_time:
    print(f"[INFO] Scheduled time {scheduled_time} UTC is in the past. Sending now...")
else:
    print(f"[INFO] Scheduled to send messages at {scheduled_time} UTC...")
    while datetime.now(timezone.utc) < scheduled_time:
        time.sleep(10)

# === Chrome Options ===
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:/Users/vprsd/chrome-selenium-profile")

# === ChromeDriver Service ===
service = Service(executable_path="C:/Users/vprsd/Downloads/chromedriver-win64/chromedriver.exe")

# === Start Chrome with Profile ===
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 30)

message_input_xpath = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[1]/p'

# === 1st Message (SYNOP) ===
driver.get("https://www.facebook.com/messages/e2ee/t/24084852691146428")
message_input = wait.until(EC.presence_of_element_located((By.XPATH, message_input_xpath)))
message_input.click()
driver.find_element(By.XPATH, message_input_xpath).send_keys(message_SYNOP)
time.sleep(5)
driver.find_element(By.XPATH, message_input_xpath).send_keys(Keys.ENTER)
time.sleep(5)
print("[SUCCESS] message_SYNOP sent.")

# === 2nd Message (Rainfall Report) ===
driver.get("https://www.facebook.com/messages/e2ee/t/27014261771521844")
message_input = wait.until(EC.presence_of_element_located((By.XPATH, message_input_xpath)))
message_input.click()
driver.find_element(By.XPATH, message_input_xpath).send_keys(message_RR)
time.sleep(5)
driver.find_element(By.XPATH, message_input_xpath).send_keys(Keys.ENTER)
time.sleep(5)
print("[SUCCESS] message_RR sent.")

# === Close the browser ===
driver.quit()
