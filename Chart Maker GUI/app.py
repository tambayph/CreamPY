import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

# Create a tkinter window
root = tk.Tk()
root.title("Image Example")

# Create a new image with a black background
image = Image.new('RGB', (400, 400), (0, 0, 0))

# Draw a red square in the center of the image
draw = ImageDraw.Draw(image)
draw.rectangle([(150, 150), (250, 250)], fill=(255, 0, 0))

# Convert the image to a PhotoImage object
photo_image = ImageTk.PhotoImage(image)



# Create a label widget to display the image
image_label = tk.Label(master=root, image=photo_image)
image_label.pack()

# Run the tkinter event loop
root.mainloop()
