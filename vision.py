# venv\Scripts\Activate  python -m streamlit run vision.py

from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load all environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(image_data, prompt, user_input):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([prompt, image_data[0], user_input])
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(
    page_title="Invoice Extractor",
    page_icon="💯"
)

st.header("💯 Invoice Application 💯")

# Provide options for uploading or capturing an image
st.subheader("Input Options")
tab1, tab2 = st.tabs(["📤 Upload Invoice", "📸 Capture Invoice"])

uploaded_file = None
captured_photo = None

# Tab for file uploader
with tab1:
    uploaded_file = st.file_uploader("Choose an invoice image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Invoice.", use_container_width=True)

# Tab for capturing photo
with tab2:
    captured_photo = st.camera_input("Take a photo of your invoice")
    if captured_photo:
        image = Image.open(captured_photo)
        st.image(image, caption="Captured Invoice.", use_container_width=True)

# Input prompt for invoice analysis
input_prompt = """
You are an expert in understanding invoices.
You will receive input images as invoices and will have to answer questions based on the input image.
"""

# User input prompt
user_input = st.text_input("Input your question about the invoice:", key="input")

if st.button("Tell me about the invoice"):
    try:
        # Choose the appropriate image source
        if uploaded_file:
            image_data = input_image_setup(uploaded_file)
        elif captured_photo:
            image_data = input_image_setup(captured_photo)
        else:
            st.error("Please upload or capture an invoice.")
            st.stop()

        # Get response from Gemini API
        response = get_gemini_response(image_data, input_prompt, user_input)
        st.subheader("The Response is:")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Styling for center alignment
page_bg_img = '''
    <style>
        h2, h3 {
            text-align: center;
        }
    </style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
