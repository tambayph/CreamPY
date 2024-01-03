from PIL import Image

folder1 = 'D:/Ezra/Python/Test/Data/deepcnn/test/23040205.jpg'
folder2 = 'D:/Ezra/Python/Test/Data/deepcnn/test/23040205.png'

# Open the input image
input_image1 = Image.open(folder1)
input_image2 = Image.open(folder2)

# Get the dimensions of the input image
width, height = input_image1.size

# Calculate the coordinates of the crop region
left = (width - 500) / 2
top = (height - 500) / 2
right = left + 500
bottom = top + 500

# Crop the image
output_image = input_image1.crop((left, top, right, bottom))

output_image = output_image.convert('RGB')

# Save the output image
output_image.save('D:/Ezra/Python/Test/Data/deepcnn/test/output_image.jpg')
