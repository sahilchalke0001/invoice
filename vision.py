from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import speech_recognition as sr
from gtts import gTTS
import tempfile

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

# Function to convert text to speech and play audio
def text_to_speech(text):
    try:
        tts = gTTS(text, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            tts.save(temp_audio.name)
            st.audio(temp_audio.name, format="audio/mp3")
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")

# Function to capture voice input and immediately process response
def get_voice_input_and_respond(image_data, prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening for your question... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio)
            st.success(f"✅ You said: {user_input}")

            # Generate response immediately
            response = get_gemini_response(image_data, prompt, user_input)
            st.subheader("The Response is:")
            st.write(response)

            # Play response audio
            text_to_speech(response)

        except sr.UnknownValueError:
            st.error("❌ Sorry, I couldn't understand the audio.")
        except sr.RequestError:
            st.error("❌ Error connecting to Google Speech API.")
        except Exception as e:
            st.error(f"⚠️ Error occurred: {str(e)}")

# Initialize Streamlit app
st.set_page_config(
    page_title="Voicy",
    page_icon="💯"
)

st.header("💯 Voicy 💯")

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

# Ensure an image is uploaded before proceeding
image_data = None
if uploaded_file:
    image_data = input_image_setup(uploaded_file)
elif captured_photo:
    image_data = input_image_setup(captured_photo)

# Text input for question
st.subheader("Ask a question about the invoice")
user_input = st.text_input("Type your question:", key="input")

# Button for voice input that automatically generates a response
if st.button("🎙️ Use Voice Input"):
    if image_data:
        get_voice_input_and_respond(image_data, input_prompt)
    else:
        st.error("⚠️ Please upload or capture an invoice first.")

# Button to analyze invoice with text input
if st.button("Ask about the Invoice"):
    if not user_input:
        st.error("⚠️ Please provide a question.")
        st.stop()
    if not image_data:
        st.error("⚠️ Please upload or capture an invoice.")
        st.stop()

    # Get response from Gemini API
    response = get_gemini_response(image_data, input_prompt, user_input)
    st.subheader("The Response is:")
    st.write(response)

    # Generate and play audio response
    text_to_speech(response)

# Styling for center alignment
page_bg_img = '''
    <style>
        h2, h3 {
            text-align: center;
        }
    </style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
