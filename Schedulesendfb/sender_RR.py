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
rainfall = input("Enter the rainfall value (in mm): ")
utz = utz = time_str.replace(":", "")
contact_name = "CMO's Visayas"
message_text = f"ROXAS {utz}Z RR={rainfall} mm"

# === Calculate Scheduled UTC Time ===
scheduled_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
print(f"[INFO] Scheduled to send to {contact_name} at {scheduled_time} UTC...")

# === Wait Until Scheduled Time in UTC ===
while datetime.now(timezone.utc) < scheduled_time:
    time.sleep(10)

# === Chrome Options ===
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:/Users/vprsd/chrome-selenium-profile")

# === ChromeDriver Service ===
service = Service(executable_path="C:/Users/vprsd/Downloads/chromedriver-win64/chromedriver.exe")

# === Start Chrome with Profile ===
driver = webdriver.Chrome(service=service, options=chrome_options)

# === Go to Facebook Messenger Chat ===
driver.get("https://www.facebook.com/messages/t/4130996670251437")

# === Wait for Message Box Using the Exact XPath ===
wait = WebDriverWait(driver, 30)
message_input_xpath = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[1]/p'

# Re-locate each time to avoid stale element
message_input = wait.until(EC.presence_of_element_located((By.XPATH, message_input_xpath)))
message_input.click()

# Type message (re-locate again just to be safe)
message_input = driver.find_element(By.XPATH, message_input_xpath)
message_input.send_keys(message_text)

# Re-locate again before pressing ENTER
message_input = driver.find_element(By.XPATH, message_input_xpath)
time.sleep(5)
message_input.send_keys(Keys.ENTER)
time.sleep(5)

print(f"[SUCCESS] Message sent to {contact_name}!")

# === Close the browser window ===
driver.quit()