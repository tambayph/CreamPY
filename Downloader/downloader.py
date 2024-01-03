# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 16:04:07 2023

@author: Ezra
"""

import datetime
import time
from selenium import webdriver

# Set the URL to screenshot
url = 'https://www.data.jma.go.jp/omaad/rsmc_nowcast/en/hcai/#zoom:5/lat:13.795406/lon:123.640137/colordepth:normal/elements:tbb&clc'

# Set the file format (can be png, jpg, or gif)
file_format = 'png'

# Specify the path to the ChromeDriver executable
chrome_driver_path = 'C:/Users/Ezra/Documents/Python Scripts/chromedriver_win32 (1)/chromedriver.exe'

# Initialize the webdriver with the path to the ChromeDriver executable
driver = webdriver.Chrome(chrome_driver_path)

# Set the size of the browser window to 1200x800 pixels
driver.set_window_size(1920, 1080)

while True:
    # Refresh the website
    driver.get(url)
    driver.refresh()

    # Wait for 10 seconds to let the page load
    time.sleep(10)

    # Get the current time and format it into a string for the filename
    current_time = datetime.datetime.now().strftime('%y%m%d%H')

    # Save the screenshot with the current time in the filename
    driver.save_screenshot(f'C:/Users/Ezra/Documents/HCAI/{current_time}.{file_format}')

    # Wait for 15 seconds before taking another screenshot
    time.sleep(3600)

# Close the webdriver
driver.quit()

