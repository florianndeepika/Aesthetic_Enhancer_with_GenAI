from dotenv import load_dotenv
load_dotenv() ## load all the environment variables from .env

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Sidebar contents
with st.sidebar:
    st.title('Aesthetics Enhancer 🏡')
    st.image(
            "https://hips.hearstapps.com/hmg-prod/images/cozy-living-room-white-1555546939.jpg",
            width = 250
        )
    st.markdown('''
    Do you want to enhance your living space with new colours and desgins?
                                
    Just upload an image of your room and gain great ideas to improve your space to a comfy cosy living space with just one click. 
    
    This is an LLM-powered application built using Google generativeai:
    - [Google Generative AI](https://ai.google/discover/generativeai/)

    ''')
    #add_vertical_space(1)
    st.write('Made with ❤️ by Floriann (Jan-2024)')
    
#function to load the google gemini pro vision api and get response
def get_gem_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

#takes uploaded imge, retirves info and returns the parts
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

##initialize our streamlit app

st.header("Aesthetics Enhancer App")

input=st.text_input("Enter your question here: ",key="input")
uploaded_file = st.file_uploader("Upload an image and click submit..", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Submit")

input_prompt="""
You are an expert in interior designing and aesthetics. 
Take note what is the preference of the user is from the input text and 
describe how the aesthetics in the image looks and
what can be changed to enhance the living space in the house 
of the image as per the user taste and expectations.
"""
## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gem_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)