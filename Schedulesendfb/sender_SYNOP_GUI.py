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

# Global flag to control cancellation
cancel_flag = threading.Event()

def start_automation():
    # Clear any previous cancel request
    cancel_flag.clear()

    # Get values from GUI
    date_str = date_entry.get()
    time_str = time_entry.get().strip()
    SYNOP = synop_entry.get("1.0", tk.END).strip()
    rainfall = rainfall_entry.get()
    rainfall24 = rainfall24_entry.get()
    TSTM = TSTM_entry.get()
    LTNG = LTNG_entry.get()

    if not date_str or not time_str or not SYNOP or not rainfall:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        utz = time_str.split(":")[0]
        message_SYNOP = f"{SYNOP}"
        message_RR = f"ROXAS {utz}00Z RR={rainfall} mm"
        message_RR24 = f"ROXAS\n0000Z RR={rainfall} mm\n24HR RR={rainfall24} mm\nTSTM={TSTM}\nLTNG={LTNG}"

        # Calculate scheduled time
        scheduled_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        now_utc = datetime.now(timezone.utc)

        if now_utc >= scheduled_time:
            log_message(f"Scheduled time {scheduled_time} UTC is in the past. Sending now...")
        else:
            log_message(f"Scheduled to send messages at {scheduled_time} UTC...")
            while datetime.now(timezone.utc) < scheduled_time:
                if cancel_flag.is_set():
                    log_message("[CANCELLED] Task stopped before sending.")
                    return
                time.sleep(1)

        if cancel_flag.is_set():
            log_message("[CANCELLED] Task stopped before sending.")
            return

        # === Chrome Options ===
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=C:/Users/vprsd/chrome-selenium-profile")

        # === ChromeDriver Service ===
        service = Service(executable_path="C:/Users/vprsd/Downloads/chromedriver-win64/chromedriver.exe")

        # === Start Chrome with Profile ===
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 30)

        message_input_xpath = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[1]/p'

        # 1st Message
        driver.get("https://www.facebook.com/messages/e2ee/t/24084852691146428")
        message_input = wait.until(EC.presence_of_element_located((By.XPATH, message_input_xpath)))
        message_input.click()
        for line in message_SYNOP.splitlines():
            driver.find_element(By.XPATH, message_input_xpath).send_keys(line)
            driver.find_element(By.XPATH, message_input_xpath).send_keys(Keys.SHIFT, Keys.ENTER)
        time.sleep(5)
        driver.find_element(By.XPATH, message_input_xpath).send_keys(Keys.ENTER)
        time.sleep(5)
        log_message("[SUCCESS] message_SYNOP sent.")

        # 2nd Message
        driver.get("https://www.facebook.com/messages/e2ee/t/27014261771521844")
        message_input = wait.until(EC.presence_of_element_located((By.XPATH, message_input_xpath)))
        message_input.click()

        # Assuming time_str is something like "00:30" or "15:45"
        hour = datetime.strptime(time_str, "%H:%M").hour

        if hour == 0:
            for line in message_RR24.splitlines():
                driver.find_element(By.XPATH, message_input_xpath).send_keys(line)
                driver.find_element(By.XPATH, message_input_xpath).send_keys(Keys.SHIFT, Keys.ENTER)
            time.sleep(5)
        else:
            driver.find_element(By.XPATH, message_input_xpath).send_keys(message_RR)
            time.sleep(5)

        driver.find_element(By.XPATH, message_input_xpath).send_keys(Keys.ENTER)
        time.sleep(5)
        log_message("[SUCCESS] Message sent.")

        driver.quit()
        log_message("[INFO] Browser closed. Done.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def log_message(msg):
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)

def run_in_thread():
    threading.Thread(target=start_automation, daemon=True).start()

def cancel_task():
    cancel_flag.set()
    log_message("[INFO] Cancel request sent.")

# === GUI ===
root = tk.Tk()
root.title("Facebook Auto/Schedule Message Sender for SYNOP and Rainfall")
root.geometry("600x450")

tk.Label(root, text="Date (click to pick):").pack()
date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
date_entry.pack()

tk.Label(root, text="Time (HH:MM, UTC): (Not applicable for 0000)").pack()
time_entry = tk.Entry(root)
time_entry.pack()

tk.Label(root, text="SYNOP:").pack()
synop_entry = tk.Text(root, height=4, width=70)
synop_entry.pack()

tk.Label(root, text="Rainfall (mm):").pack()
rainfall_entry = tk.Entry(root)
rainfall_entry.pack()

tk.Label(root, text="24HR RR (mm):").pack()
rainfall24_entry = tk.Entry(root)
rainfall24_entry.pack()

tk.Label(root, text="TSTM:").pack()
TSTM_entry = tk.Entry(root)
TSTM_entry.pack()

tk.Label(root, text="LTNG:").pack()
LTNG_entry = tk.Entry(root)
LTNG_entry.pack()

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Submit", command=run_in_thread).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Cancel", command=cancel_task).grid(row=0, column=1, padx=5)

log_text = tk.Text(root, height=10, width=50)
log_text.pack()

root.mainloop()
