import tkinter as tk
import customtkinter
from PIL import Image, ImageTk

# import sys
# sys.path.append('D:/Ezra/Python/Scripts/Tropical Cyclone Work Station/Functions')
import Button_Functions as BF

##########################################################################################################
##########################################################################################################

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry('800x800')
root.title('Tropical Cyclone Work Station')

##########################################################################################################
##########################################################################################################

frame1 = customtkinter.CTkFrame(master=root,width=400, height=400)
frame1.pack(side='left', pady=20, padx=20, fill='both', expand=True)

# Create a label
label = customtkinter.CTkLabel(master=frame1, text='Tropical Cyclone Track Maker', font=('Roboto', 18))
label.pack(side='top', anchor='nw', padx=20, pady=10)

# Create a frame to hold the directory selection button and textbox
frame2 = customtkinter.CTkFrame(master=frame1)
frame2.pack(side='bottom', anchor='sw', padx=20, pady=10)
button1 = customtkinter.CTkButton(master=frame2, text='Generate Chart', width=410, command=lambda:BF.generatemap())
button1.pack(side='left')

frame3 = customtkinter.CTkFrame(master=frame1)
frame3.pack(side='bottom', anchor='sw', padx=20, pady=10)
button2 = customtkinter.CTkButton(master=frame3, text='Save Chart at', width=150, command=lambda: BF.choose_directory(textbox1))
button2.pack(side='left')
textbox1 = tk.Text(master=frame3,width=30, height=1.4)
textbox1.pack(side='left', padx=10)

frame4 = customtkinter.CTkFrame(master=frame1)
frame4.pack(side='bottom', anchor='sw', padx=20, pady=10)
button3 = customtkinter.CTkButton(master=frame4, text='Track Input', width=150, command=lambda: BF.browse_and_insert(textbox2))
button3.pack(side='left')
textbox2 = tk.Text(master=frame4,width=30, height=1.4)
textbox2.pack(side='left', padx=10)


# Create a frame to hold the image
frame5 = customtkinter.CTkFrame(master=frame1)
frame5.pack(side='top', anchor='nw', padx=20, pady=10)

# Load the image and create a PhotoImage object
image_path = 'C:/Users/WF026/Desktop/Tropical Cyclone Work Station/Images/png.png'
image = Image.open(image_path)
resized_image = image.resize((700, 800)) # Resize the image to 400x400 pixels
photo_image = ImageTk.PhotoImage(resized_image)

# Create a Label widget to display the image
image_label = tk.Label(master=frame5, image=photo_image, width=700, height=800)
image_label.image = photo_image # keep a reference to the image object
image_label.pack(side='left')

##########################################################################################################
##########################################################################################################

framea = customtkinter.CTkFrame(master=root,width=800, height=800)
framea.pack(side='left', pady=20, padx=20, fill='both', expand=True)

# Create a label
labela = customtkinter.CTkLabel(master=framea, text='Rainfall Maker', font=('Roboto', 18))
labela.pack(side='top', anchor='nw', padx=20, pady=10)

# Create a frame to hold the image
framea5 = customtkinter.CTkFrame(master=framea)
framea5.pack(side='top', anchor='nw', padx=20, pady=10)

# Load the image and create a PhotoImage object
image_patha = 'C:/Users/WF026/Desktop/Tropical Cyclone Work Station/Images/png.png'
imagea = Image.open(image_patha)
resized_imagea = image.resize((700, 800)) # Resize the image to 400x400 pixels
photo_imagea = ImageTk.PhotoImage(resized_imagea)

# Create a Label widget to display the image
image_labela = tk.Label(master=framea5, image=photo_imagea, width=700, height=800)
image_labela.image = photo_imagea # keep a reference to the image object
image_labela.pack(side='left')

root.mainloop()





