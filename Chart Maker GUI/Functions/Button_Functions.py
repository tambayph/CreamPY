from tkinter import filedialog       
import os
import time
import Track_Maker
import subprocess
from PIL import Image, ImageTk
import tkinter as tk

def browse_and_insert(textbox):
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if file_path:
        directory_path = os.path.dirname(file_path)
        textbox.insert('end', directory_path)
        # Track_Maker.file = directory_path
                
def choose_directory(textbox):
    directory_path = filedialog.askdirectory()
    textbox.delete('1.0', 'end') # Clear the textbox
    textbox.insert('end', directory_path)        
    # Track_Maker.savedir = directory_path   


def generatemap():
    subprocess.run(['python', 'C:/Users/WF026/Desktop/Tropical Cyclone Work Station/Track_Maker.py'])
    # Wait for the file to be created
while not os.path.exists('C:/Users/WF026/Desktop/Tropical Cyclone Work Station/Images/output.jpg'):
    time.sleep(1)
    # Load the image and create a PhotoImage object
    image_path = 'C:/Users/WF026/Desktop/Tropical Cyclone Work Station/Images/output.jpg'
    image = Image.open(image_path)
    resized_image = image.resize((700, 800)) # Resize the image to 400x400 pixels
    photo_image = ImageTk.PhotoImage(resized_image)

    # Create a Label widget to display the image
    image_label = tk.Label(master=frame5, image=photo_image, width=700, height=800)
    image_label.image = photo_image # keep a reference to the image object
    image_label.pack(side='left')

    
    
    