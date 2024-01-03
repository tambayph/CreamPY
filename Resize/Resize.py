# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 15:49:45 2023

@author: WF026
"""

from PIL import Image
import os

# Path to the folder containing the images you want to resize
folder_path = 'D:/Ezra/Python/Test/images'

# Desired size of the images after resizing
desired_size = (3825, 4950)

# Loop over all the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Open the image using Pillow
        image = Image.open(os.path.join(folder_path, filename))

        # Resize the image
        resized_image = image.resize(desired_size, resample=Image.LANCZOS)

        # Save the resized image with the same filename
        resized_image.save(os.path.join(folder_path, filename))
