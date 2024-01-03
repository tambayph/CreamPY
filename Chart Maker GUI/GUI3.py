# -*- coding: utf-8 -*-
"""
Created on Tue May 16 13:11:54 2023

@author: WF026
"""
import tkinter as tk
import customtkinter
import Button_Functions as BF
from PIL import Image, ImageTk

###############################################################################
###############################################################################    

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry('800x800')
root.title('Tropical Cyclone Work Station')

###############################################################################
###############################################################################

framea = customtkinter.CTkFrame(master=root,width=400, height=400)
framea.pack(side='left', pady=20, padx=20, fill='both', expand=True)

# Create a label
label = customtkinter.CTkLabel(master=framea, text='Tropical Cyclone Track Maker', font=('Roboto', 18))
label.pack(side='top', anchor='nw', padx=20, pady=10)

# Create a frame to hold the directory selection button and textbox
frame2 = customtkinter.CTkFrame(master=framea)
frame2.pack(side='bottom', anchor='sw', padx=20, pady=10)
button1 = customtkinter.CTkButton(master=frame2, text='Generate Chart', width=410, command=lambda: BF.generate_image(image_label))
button1.pack(side='left')

frame3 = customtkinter.CTkFrame(master=framea)
frame3.pack(side='bottom', anchor='sw', padx=20, pady=10)
button2 = customtkinter.CTkButton(master=frame3, text='Save Chart at', width=150, command=lambda: BF.choose_directory(textbox1))
button2.pack(side='left')
textbox1 = tk.Text(master=frame3,width=30, height=1.4)
textbox1.pack(side='left', padx=10)

frame4 = customtkinter.CTkFrame(master=framea)
frame4.pack(side='bottom', anchor='sw', padx=20, pady=10)
button3 = customtkinter.CTkButton(master=frame4, text='Track Input', width=150, command=lambda: BF.browse_and_insert(textbox2))
button3.pack(side='left')
textbox2 = tk.Text(master=frame4,width=30, height=1.4)
textbox2.pack(side='left', padx=10)

frame5 = customtkinter.CTkFrame(master=framea, width=800, height=800)
frame5.pack(side='bottom', anchor='sw', padx=20, pady=10)

image_path = "C:/Users/WF026/Desktop/Tropical Cyclone Work Station/Images/doraemon.jpg"
image = Image.open(image_path)
resized_image = image.resize((600, 800))
photo_image = ImageTk.PhotoImage(resized_image)
image_label = customtkinter.CTkLabel(master=frame5, image = photo_image)
image_label.pack()

###############################################################################
###############################################################################
frameb = customtkinter.CTkFrame(master=root,width=400, height=400)
frameb.pack(side='right', pady=20, padx=20, fill='both', expand=True)

# Create a label
labelb = customtkinter.CTkLabel(master=frameb, text='Tropical Cyclone Rainfall Maker', font=('Roboto', 18))
labelb.pack(side='top', anchor='nw', padx=20, pady=10)

# Create a frame to hold the directory selection button and textbox
frame2b = customtkinter.CTkFrame(master=frameb)
frame2b.pack(side='bottom', anchor='sw', padx=20, pady=10)
button1b = customtkinter.CTkButton(master=frame2b, text='Generate Chart', width=410, command=lambda: BF.generate_imageb(image_labelb))
button1b.pack(side='left')

frame3b = customtkinter.CTkFrame(master=frameb)
frame3b.pack(side='bottom', anchor='sw', padx=20, pady=10)
button2b = customtkinter.CTkButton(master=frame3b, text='Save Chart at', width=150, command=lambda: BF.choose_directoryb(textbox1b))
button2b.pack(side='left')
textbox1b = tk.Text(master=frame3b,width=30, height=1.4)
textbox1b.pack(side='left', padx=10)

frame7b = customtkinter.CTkFrame(master=frameb)
frame7b.pack(side='bottom', anchor='sw', padx=20, pady=10)
button5b = customtkinter.CTkButton(master=frame7b, text='Rainfall Input', width=150, command=lambda: BF.browse_and_insertc(textbox4b))
button5b.pack(side='left')
textbox4b = tk.Text(master=frame7b,width=30, height=1.4)
textbox4b.pack(side='left', padx=10)

frame6b = customtkinter.CTkFrame(master=frameb)
frame6b.pack(side='bottom', anchor='sw', padx=20, pady=10)
button4b = customtkinter.CTkButton(master=frame6b, text='GSMAP Input', width=150, command=lambda: BF.choose_directoryc(textbox3b))
button4b.pack(side='left')
textbox3b = tk.Text(master=frame6b,width=30, height=1.4)
textbox3b.pack(side='left', padx=10)

frame4b = customtkinter.CTkFrame(master=frameb)
frame4b.pack(side='bottom', anchor='sw', padx=20, pady=10)
button3b = customtkinter.CTkButton(master=frame4b, text='Track Input', width=150, command=lambda: BF.browse_and_insertb(textbox2b))
button3b.pack(side='left')
textbox2b = tk.Text(master=frame4b,width=30, height=1.4)
textbox2b.pack(side='left', padx=10)

frame5b = customtkinter.CTkFrame(master=frameb, width=800, height=800)
frame5b.pack(side='bottom', anchor='sw', padx=20, pady=10)
image_pathb = "C:/Users/WF026/Desktop/Tropical Cyclone Work Station/Images/doraemon.jpg"
imageb = Image.open(image_pathb)
resized_imageb = imageb.resize((600, 800))
photo_imageb = ImageTk.PhotoImage(resized_imageb)
image_labelb = customtkinter.CTkLabel(master=frame5b, image = photo_imageb)
image_labelb.pack()
###############################################################################
###############################################################################
root.mainloop()
