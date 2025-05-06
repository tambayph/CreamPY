from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime

# === Input Section ===
date_str = input("Enter the date (YYYY-MM-DD): ")
time_str = input("Enter the time (HH:MM, 24-hour format): ")
rainfall = input("Enter the rainfall value (in mm): ")

contact_name = "Jun Ezra Bulquerin"
message_text = f"🌧️ Rainfall Report\nDate: {date_str}\nTime: {time_str}\nRainfall: {rainfall} mm"

# === Calculate Scheduled Time ===
scheduled_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
print(f"[INFO] Scheduled to send to {contact_name} at {scheduled_time}...")

# === Wait Until Scheduled Time ===
while datetime.now() < scheduled_time:
    time.sleep(10)

# === Set up Chrome with persistent user profile ===
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:/Users/vprsd20/AppData/Local/Google/Chrome/User Data")  # ← Replace with your path
chrome_options.add_argument("profile-directory=Default")  # Uses your default Chrome profile

# === Launch Chrome and Open Messenger ===
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.facebook.com/messages/t/")

# Optional: Wait for page load if needed
time.sleep(5)

# === Find the Contact ===
search_box = driver.find_element(By.XPATH, '//input[@placeholder="Search Messenger"]')
search_box.send_keys(contact_name)
search_box.send_keys(Keys.RETURN)
time.sleep(4)

# === Send the Message ===
message_box = driver.switch_to.active_element
message_box.send_keys(message_text)
message_box.send_keys(Keys.RETURN)

print(f"[SUCCESS] Message sent to {contact_name}!")
