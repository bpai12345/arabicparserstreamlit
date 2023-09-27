import streamlit as st
import fitz
import os
from ArabicOcr import arabicocr
from io import BytesIO
from PIL import Image

# Create a Streamlit app title
st.title("PDF to Image and Arabic Text Extraction")

# Create a file upload widget
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Check if a file is uploaded
if uploaded_file:
    # Read the uploaded PDF file
    pdf_content = uploaded_file.read()

    # Save the uploaded PDF as a temporary file
    with open("arabic_image.pdf", "wb") as temp_pdf:
        temp_pdf.write(pdf_content)

    # Open the uploaded PDF file
    doc = fitz.open("arabic_image.pdf")

    # Create columns for layout
    col1, col2 = st.columns(2)

    # Select a page
    with col1:
        # Create a dropdown to select a page
        page_number = st.selectbox("Select a Page", range(len(doc)))

        # Get the selected page
        page = doc[page_number]

        # Render the page to an image
        pixmap = page.get_pixmap()
        
        # Save the pixmap as a temporary PNG file
        temp_image_path = f"temp_image.png"
        pixmap.writePNG(temp_image_path)

        # Display the image
        st.image(Image.open(temp_image_path))

    # Perform Arabic OCR on the selected page
    image_path = f"page-{page_number}.png"
    out_image = 'out.jpg'
    results = arabicocr.arabic_ocr(image_path, out_image)

    # Extract and display the text
    words = [result[1] for result in results]
    text = " ".join(words)

    # Display the text in the right column
    with col2:
        st.header("Extracted Text")
        st.text(text)

    # Save the extracted text as a text file
    with open('file.txt', 'w', encoding='utf-8') as myfile:
        myfile.write(text)

    # Clean up the temporary PNG file
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)

# Clean up the temporary PDF file after processing
if os.path.exists("arabic_image.pdf"):
    os.remove("arabic_image.pdf")
