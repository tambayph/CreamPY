import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timezone
import threading
from tkcalendar import DateEntry
from datetime import datetime, timezone
import calendar
import os

# === Your existing constants ===
CONTACT_NAME = "ATS-PAGASA"
MESSAGE_URL = "https://www.facebook.com/messages/t/6623903127675852"
# MESSAGE_URL = "https://www.facebook.com/messages/e2ee/t/27014261771521844" #sample
CHROME_PROFILE_PATH = "user-data-dir=C:/Users/vprsd/chrome-selenium-profile"
CHROMEDRIVER_PATH = "C:/chromedriver-win64/chromedriver.exe"
MESSAGE_INPUT_XPATH = (
    '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/'
    'div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[1]/p'
)

cancel_flag = False  # Flag to cancel the scheduled send

# === Function to log messages to the log box ===
def log_message(msg):
    log_box.config(state="normal")
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)  # Auto-scroll
    log_box.config(state="disabled")

# === Function to save sent messages to a txt file ===
def save_sent_message(metar):
    try:
        # Get current UTC time
        now = datetime.now(timezone.utc)

        # Build the filename dynamically based on current month/year
        month_num = now.strftime("%m")          # e.g. "10"
        month_abbr = now.strftime("%b").upper() # e.g. "OCT"
        year_suffix = now.strftime("%y")        # e.g. "25"
        filename = f"{month_num} {month_abbr}_{year_suffix}.txt"

        # Define full path
        folder = f"G:/My Drive/METAR/{now.strftime('%Y')}"
        os.makedirs(folder, exist_ok=True)  # Create folder if it doesn't exist
        filepath = os.path.join(folder, filename)

        # Write the METAR message
        timestamp = now.strftime("%H%M")  # UTC time
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"\n{metar}/{timestamp}")

        log_message(f"[INFO] Message saved to {filename} (UTC time)")

    except Exception as e:
        log_message(f"[ERROR] Could not save message: {e}")

def send_message(date_str, time_str, metar):
    global cancel_flag
    try:
        cancel_flag = False
        scheduled_time = datetime.strptime(
            f"{date_str} {time_str}", "%Y-%m-%d %H:%M"
        ).replace(tzinfo=timezone.utc)

        now_utc = datetime.now(timezone.utc)

        if now_utc < scheduled_time:
            log_message(f"[INFO] Waiting until {scheduled_time} UTC...")
            while datetime.now(timezone.utc) < scheduled_time:
                if cancel_flag:
                    log_message("[INFO] Sending canceled by user.")
                    messagebox.showinfo("Canceled", "Message sending was canceled.")
                    return
                time.sleep(10)
        else:
            log_message("[INFO] Time is now or past, sending immediately.")

        # === Chrome Options ===
        chrome_options = Options()
        chrome_options.add_argument(CHROME_PROFILE_PATH)

        # === ChromeDriver Service ===
        service = Service(executable_path=CHROMEDRIVER_PATH)

        # === Start Chrome with Profile ===
        log_message("[INFO] Launching Chrome browser...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(MESSAGE_URL)

        wait = WebDriverWait(driver, 30)
        message_input = wait.until(
            EC.presence_of_element_located((By.XPATH, MESSAGE_INPUT_XPATH))
        )
        message_input.click()
        message_input = driver.find_element(By.XPATH, MESSAGE_INPUT_XPATH)
        message_input.send_keys(metar)
        time.sleep(5)
        message_input.send_keys(Keys.ENTER)
        time.sleep(5)

        log_message(f"[SUCCESS] Message sent to {CONTACT_NAME}!")

        # === Save sent message to file ===
        save_sent_message(metar)

        driver.quit()
        messagebox.showinfo("Success", f"Message sent to {CONTACT_NAME}!")
    except Exception as e:
        log_message(f"[ERROR] {str(e)}")
        messagebox.showerror("Error", str(e))

# === Tkinter GUI ===
def on_send():
    date_str = date_entry.get()
    time_str = time_entry.get()
    metar = metar_entry.get("1.0", tk.END).strip()

    if not date_str or not time_str or not metar:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    log_message(f"[INFO] Scheduled message for {date_str} {time_str} UTC")
    threading.Thread(target=send_message, args=(date_str, time_str, metar), daemon=True).start()

def on_cancel():
    global cancel_flag
    cancel_flag = True
    log_message("[INFO] Cancel request received.")

root = tk.Tk()
root.title("METAR Auto/Schedule Messenger")
root.geometry("500x400")

tk.Label(root, text="Date (click to pick):").pack()
date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
date_entry.pack()

tk.Label(root, text="Time (HH:MM, UTC):").pack(pady=5)
time_entry = tk.Entry(root)
time_entry.pack()

tk.Label(root, text="METAR:").pack(pady=5)
metar_entry = tk.Text(root, height=3, width=50)
metar_entry.pack()

frame = tk.Frame(root)
frame.pack(pady=10)

send_button = tk.Button(frame, text="Send Message", command=on_send)
send_button.pack(side=tk.LEFT, padx=5)

cancel_button = tk.Button(frame, text="Cancel", command=on_cancel)
cancel_button.pack(side=tk.LEFT, padx=5)

# === Log Box ===
log_box = tk.Text(root, height=10, width=50)
log_box.pack()

root.mainloop()
