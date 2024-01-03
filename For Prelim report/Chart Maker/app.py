# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 06:57:24 2023

@author: WF026
"""

import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import subprocess 

class TCWorkstationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chart Maker")

        self.tcid_label = ttk.Label(root, text="TCID:")
        self.tcid_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.tcid_entry = ttk.Entry(root)
        self.tcid_entry.grid(row=0, column=1, padx=10, pady=10)

        self.local_name_label = ttk.Label(root, text="Local Name:")
        self.local_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.local_name_entry = ttk.Entry(root)
        self.local_name_entry.grid(row=1, column=1, padx=10, pady=10)

        self.generate_button = ttk.Button(root, text="Generate Chart", command=self.generate_chart)
        self.generate_button.grid(row=2, columnspan=2, padx=10, pady=20)
        
        italics_font = Font(slant="italic")
        self.info_label = ttk.Label(root, text="*Charts will be automatically downloaded in the Downloads folder.", font=italics_font)
        self.info_label.grid(row=3, columnspan=2, padx=1, pady=1)

    def generate_chart(self):
        tcid = self.tcid_entry.get()
        local_name = self.local_name_entry.get()
        
        with open("input.txt", "w") as file:
            file.write(f"{tcid}\n")
            file.write(f"{local_name}\n")
        # Run the chart generation script as a subprocess
        subprocess.run(["python", "Track Maker.py"])
        subprocess.run(["python", "Signal Chart.py"])
        subprocess.run(["python", "Rainfall Chart.py"])

def main():
    root = tk.Tk()
    app = TCWorkstationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

