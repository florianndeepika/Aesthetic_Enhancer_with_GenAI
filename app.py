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
    st.write('Made with ❤️ by Floriann (Jan-2024)')
    st.image(
            "https://hips.hearstapps.com/hmg-prod/images/cozy-living-room-white-1555546939.jpg",
            width = 200
        )
    st.markdown('''
    Do you want to enhance your living space with new colours and designs?
                                
    Just upload an image of your room and ask your questions to gain great ideas to have a comfy cosy living space with just one click. 
    
    This is an LLM-powered application built using Google generativeai:
    - [Google Generative AI](https://ai.google/discover/generativeai/)

    ''')
    
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
input=st.text_input("Enter your question here: Can I paint my wall Ivory? Will plants enhance my living space?",key="input")

uploaded_file = st.file_uploader("Upload an image and click submit..", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Submit")

input_prompt="""
Act as an interior designing consultant having interior designer creativity, design skills, and attention to detail,
Assess the space in the image and describe the beauty of the space such as colours, lighting, and materials in the image.
Answer the client question from the input box as an interior designing client consultant.
Additionally, provide some additional tips to enhgance the space by keeping in mind the factors such as interior design concepts, 
colour schemes, design concepts, furniture placement,and functionality to create a practical design in the following format,
1.
2.
3.
..
 """
st.write('Note : Google Gen AI is an open-source LLM model which collects user data')
## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gem_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)
