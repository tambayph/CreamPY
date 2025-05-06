from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import pandas as pd
from fpdf import FPDF

x = "DATE VARIABLE"
y = "CONSTRUCTION COMPANY VARIABLE"
z = "AMOUNT VARIABLE"
a = "DATE RANGE VARIABLE"

def create_pdf():
    # Create a PDF file named 'rainfall_report.pdf'
    c = canvas.Canvas("rainfall_report.pdf", pagesize=letter)
    width, height = letter

    # Set font for the document
    c.setFont("Helvetica", 12)

    # Centered text function
    def draw_centered_text(y_position, text, font="Helvetica", size=12):
        text_width = c.stringWidth(text, font, size)  # Get the width of the text
        x_position = (width - text_width) / 2  # Calculate the x-position for centering
        c.setFont(font, size)  # Set font for this text
        c.drawString(x_position, y_position, text)

    # For right-aligned text, we need to calculate the x-coordinate based on the width
    date_text_width = c.stringWidth("Date: __________________", "Helvetica", 12)

    # # Draw the logo (replace 'logo.png' with the path to your logo file)
    # logo_path = "logo.jpg"  # Change to your actual logo path
    # logo_width = 140  # Adjust the logo width
    # logo_height = 100  # Adjust the logo height
    # logo_x_position = width - 570  # Center the logo horizontally
    # logo_y_position = height - 115  # Set the vertical position for the logo

    # # Draw the logo image at the specified position
    # c.drawImage(logo_path, logo_x_position, logo_y_position, width=logo_width, height=logo_height)


    # # Write centered content to the PDF
    # draw_centered_text(height - 40, "Republic of the Philippines")
    # draw_centered_text(height - 55, "Department of Science and Technology", font="Helvetica-Bold")
    # draw_centered_text(height - 70, "Philippine Atmospheric, Geophysical and Astronomical", font="Helvetica-Bold")
    # draw_centered_text(height - 85, "Services Administration (PAGASA)", font="Helvetica-Bold")
    # draw_centered_text(height - 100, "Airport, Roxas City")



    # c.drawString(width - 10 - date_text_width, height - 140, "Date: _____________")

    # draw_centered_text(height - 180, "ACKNOWLEDGEMENT RECEIPT", size=15, font="Helvetica-Bold")

    # # Set font for the document
    # c.setFont("Helvetica", 12)

    # # Write the additional content with left-aligned text
    # c.drawString(50, height - 215, "This is to acknowledge the receipt from _______________________________________________")
    

    # c.drawString(50, height - 235, "The amount of (Php) _________________________ as payment of weather certification containing")
    # c.drawString(50, height - 255, "daily rainfall data for the month: _____________________________________________________")
    # c.drawString(50, height - 275, "_______________________________________________________________________________")
    # c.drawString(50, height - 295, "")

    # c.setFont("Helvetica-Bold", 12)  # Set font to bold for this line

    # c.drawString(width + 20 - date_text_width, height - 138, x)

    # c.drawString(270, height - 213, y)
    # c.drawString(190, height - 232, z)
    # c.drawString(265, height - 253, a)

    # c.drawString(width - 100 - date_text_width, height - 335, "Payment received by:")
    # c.setFont("Helvetica-Bold", 12)
    # c.drawString(width - 50 - date_text_width, height - 385, "JUN EZRA M. BULQUERIN")
    # c.setFont("Helvetica", 12)
    # c.drawString(width - 50 - date_text_width, height - 400, "CMO") 
    # c.drawString(width - 50 - date_text_width, height - 415, "PAGASA ROXAS CITY")

    # # Start a new page for the next section
    # c.showPage()

    # # Draw the logo (replace 'logo.png' with the path to your logo file)
    # logo_path = "logo.jpg"  # Change to your actual logo path
    # logo_width = 140  # Adjust the logo width
    # logo_height = 100  # Adjust the logo height
    # logo_x_position = width - 570  # Center the logo horizontally
    # logo_y_position = height - 115  # Set the vertical position for the logo

    # # Draw the logo image at the specified position
    # c.drawImage(logo_path, logo_x_position, logo_y_position, width=logo_width, height=logo_height)

    # # Write centered content to the PDF
    # draw_centered_text(height - 40, "Republic of the Philippines")
    # draw_centered_text(height - 55, "Department of Science and Technology", font="Helvetica-Bold")
    # draw_centered_text(height - 70, "Philippine Atmospheric, Geophysical and Astronomical", font="Helvetica-Bold")
    # draw_centered_text(height - 85, "Services Administration (PAGASA)", font="Helvetica-Bold")
    # draw_centered_text(height - 100, "Airport, Roxas City")

    # c.drawString(width + 20 - date_text_width, height - 138, x)

    # # Page 2 - Letter content for MARY JEAN R. BARCELONA
    # c.setFont("Helvetica-Bold", 12)
    # c.drawString(50, height - 180, "MARY JEAN R. BARCELONA")
    # c.setFont("Helvetica", 12)
    # c.drawString(50, height - 200, "Owner/Proprietress")
    # c.drawString(50, height - 220, "MJ BARCELONA CONSTRUCTION AND SUPPLY")

    # c.drawString(50, height - 270, "Sir/Maam:")
    # c.drawString(50, height - 300, "In reference to your request, please find attached the rainfall data extracted from our official weather") 
    # c.drawString(50, height - 320, "observation records for the period of") 
    # c.setFont("Helvetica-Bold", 12)
    # c.drawString(245, height - 320, a) 

    # c.setFont("Helvetica", 12)
    # c.drawString(390, height - 320, ".") 
    # c.drawString(50, height - 350, "Should you require any further information or have any questions regarding the data, please do not") 
    # c.drawString(50, height - 370, "hesitate to contact us.") 

    # c.drawString(width - 30 - date_text_width, height - 450, "Best regards,")
    # c.setFont("Helvetica-Bold", 12)
    # c.drawString(width - 30 - date_text_width, height - 500, "JUN EZRA M. BULQUERIN")
    # c.setFont("Helvetica", 12)
    # c.drawString(width - 30 - date_text_width, height - 520, "CMO") 
    # c.drawString(width - 30 - date_text_width, height - 540, "PAGASA ROXAS CITY")

    # # Start a new page for the next section
    # c.showPage()

    # Draw the logo (replace 'logo.png' with the path to your logo file)
    logo_path = "logo.jpg"  # Change to your actual logo path
    logo_width = 140  # Adjust the logo width
    logo_height = 100  # Adjust the logo height
    logo_x_position = width - 570  # Center the logo horizontally
    logo_y_position = height - 115  # Set the vertical position for the logo

    # Draw the logo image at the specified position
    c.drawImage(logo_path, logo_x_position, logo_y_position, width=logo_width, height=logo_height)

    # Write centered content to the PDF
    draw_centered_text(height - 40, "Republic of the Philippines")
    draw_centered_text(height - 55, "Department of Science and Technology", font="Helvetica-Bold")
    draw_centered_text(height - 70, "Philippine Atmospheric, Geophysical and Astronomical", font="Helvetica-Bold")
    draw_centered_text(height - 85, "Services Administration (PAGASA)", font="Helvetica-Bold")
    draw_centered_text(height - 100, "Airport, Roxas City")

    c.drawString(width + 20 - date_text_width, height - 138, x)

    c.drawString(50, height - 180, "The following rainfall data are extracted from our official weather observation record covering the") 
    c.drawString(50, height - 200, "month of")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 200, "DATE VARIABLE")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 220, "This data is issued upon the request of") 
    c.setFont("Helvetica-Bold", 12)
    c.drawString(260, height - 220, "CONSTRUCTION COMPANY VARIABLE.") 

    df = pd.read_excel('rainfalldb.xlsx')       

    # Step 2: Filter data for a specific year and month
    year_filter = 2000  # Specify the year
    month_filter = 1   # Specify the month

    filtered_df = df[(df['year'] == year_filter) & (df['month'] == month_filter)]
    c.drawString(200, height - 240, f"Rainfall Data - {year_filter}-{month_filter:02d}")




    # Save the PDF
    c.save()

# Run the function to create the PDF
create_pdf()
