import streamlit as st
import os
import fitz  # PyMuPDF
from PIL import Image
from ArabicOcr import arabicocr
from PIL import Image, ImageOps

#Make streamlit to wide screen
st.set_page_config(layout="wide")

# Hide made with streamlit and Hamburger menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 



# Uploading file in the form of pdf, doc and docx format 
image = Image.open(r'BPAI_logo.png')
st.image(image)
st.header("ARABIC PARSER")

# Create a file upload widget
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Check if a file is uploaded
if uploaded_file:
    # Save the uploaded PDF as a temporary file
    with open("arabic_pdf.pdf", "wb") as temp_pdf:
        temp_pdf.write(uploaded_file.read())

    # Open the PDF using PyMuPDF (Fitz)
    pdf_document = fitz.open("arabic_pdf.pdf")

    # Create a folder to store images
    os.makedirs("pdf_images", exist_ok=True)

    # Convert PDF pages to images
    image_paths = []
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        image = page.get_pixmap()
        image_path = os.path.join("pdf_images", f"page_{page_number}.png")
        image.save(image_path)
        image_paths.append(image_path)

    # Perform Arabic OCR on the images and extract text
    extracted_text = []
    out_image = 'out.jpg'
    for image_path in image_paths:
        results = arabicocr.arabic_ocr(image_path, out_image)
        words = [result[1] for result in results]
        text = " ".join(words)
        extracted_text.append(text)

    # Combine extracted text from all images
    text = "\n".join(extracted_text)

    # Display the extracted text in a scrollable text area
    st.header("Extracted Text")
    st.text_area("Extracted Arabic Text", text, height=400)
