import subprocess
from tkinter import filedialog       
import os
import time
from PIL import Image, ImageTk

selected_file_dir = None
selected_file_dirb = None
selected_file_dirc = None

selected_file_path = None
selected_file_pathb = None
selected_file_pathc = None

def browse_and_insert(textbox2):
    global selected_file_path
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if file_path:
        textbox2.delete('1.0', 'end') # Clear the textbox
        textbox2.insert('end', file_path)
        selected_file_path = file_path

def choose_directory(textbox1):
    global selected_file_dir
    file_path1 = filedialog.asksaveasfilename(filetypes=[('Image Files', '*.jpg')])
    textbox1.delete('1.0', 'end')  # Clear the textbox
    textbox1.insert('end', file_path1)    
    selected_file_dir = file_path1

def generate_image(image_label):
    with open("input.txt", "w") as file:
        file.write(f"{selected_file_path}\n")
        file.write(f"{selected_file_dir}\n")
    subprocess.run(['python', 'C:/Users/WF026/Desktop/Tropical Cyclone Work Station/Track_Maker.py'])
    
    # Wait for the file to be created
    while not os.path.exists(selected_file_dir):
        time.sleep(5)

    # Load the image and create a PhotoImage object
    image_path = selected_file_dir
    image = Image.open(image_path)
    resized_image = image.resize((800, 800)) # Resize the image to 400x400 pixels
    photo_image = ImageTk.PhotoImage(resized_image)

    # Update the image label with the new image
    image_label.configure(image=photo_image)
    image_label.image = photo_image # keep a reference to the image object    
    
def browse_and_insertb(textbox2b):
    global selected_file_pathb
    file_pathb = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if file_pathb:
        textbox2b.delete('1.0', 'end') # Clear the textbox
        textbox2b.insert('end', file_pathb)
        selected_file_pathb = file_pathb
        
def browse_and_insertc(textbox4b):
    global selected_file_pathc
    file_pathc = filedialog.askopenfilename(filetypes=[('Excel Files', '*.csv')])
    if file_pathc:
        textbox4b.delete('1.0', 'end') # Clear the textbox
        textbox4b.insert('end', file_pathc)
        selected_file_pathc = file_pathc        
        
def choose_directoryb(textbox1b):
    global selected_file_dirb
    file_pathe = filedialog.asksaveasfilename(filetypes=[('Image Files', '*.jpg')])
    textbox1b.delete('1.0', 'end')  # Clear the textbox
    textbox1b.insert('end', file_pathe)    
    selected_file_dirb = file_pathe        

def choose_directoryc(textbox3b):
    global selected_file_dirc
    file_pathf = filedialog.askdirectory()
    textbox3b.delete('1.0', 'end')  # Clear the textbox
    textbox3b.insert('end', file_pathf)    
    selected_file_dirc = file_pathf 
    
def generate_imageb(image_labelb):
    with open("inputb.txt", "w") as file:
        file.write(f"{selected_file_pathb}\n")
        file.write(f"{selected_file_dirc}\n")
        file.write(f"{selected_file_pathc}\n")
        file.write(f"{selected_file_dirb}\n")
    subprocess.run(['python', 'C:/Users/WF026/Desktop/Tropical Cyclone Work Station/GSMAP_overlay_SYNOP_Per_TC.py'])
    
    # Wait for the file to be created
    while not os.path.exists(selected_file_dirb):
        time.sleep(5)

    # Load the image and create a PhotoImage object
    image_pathb = selected_file_dirb
    imageb = Image.open(image_pathb)
    resized_imageb = imageb.resize((800, 800)) # Resize the image to 400x400 pixels
    photo_imageb = ImageTk.PhotoImage(resized_imageb)

    # Update the image label with the new image
    image_labelb.configure(image=photo_imageb)
    image_labelb.image = photo_imageb # keep a reference to the image object    