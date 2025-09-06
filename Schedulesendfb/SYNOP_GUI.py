import tkinter as tk
from tkinter import messagebox
import subprocess

def send_sms():
    number = entry_number.get()
    msg = entry_msg.get("1.0", tk.END).strip()
    if not number or not msg:
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        # ADB command to send SMS (works on many Android versions)
        cmd = f'adb shell am start -a android.intent.action.SENDTO -d sms:{number} --es sms_body "{msg}" --ez exit_on_sent true'
        subprocess.run(cmd, shell=True)
        messagebox.showinfo("Success", f"Message sent to {number}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("SMS Sender")

tk.Label(root, text="Phone Number:").pack()
entry_number = tk.Entry(root, width=30)
entry_number.pack()

tk.Label(root, text="Message:").pack()
entry_msg = tk.Text(root, width=40, height=5)
entry_msg.pack()

tk.Button(root, text="Send SMS", command=send_sms).pack()

root.mainloop()
