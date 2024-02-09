import streamlit as st
import os

from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

#Load API Key
load_dotenv() ## load all the environment variables
genai.configure(api_key='AIzaSyAnXA5TY6uVWXNNv-r4utsFXOA9nqh5IBU')

# Creating a generative model Instance
model=genai.GenerativeModel('gemini-pro-vision')

#creating a function to get image details
def input_image_details(upload_file):
    if upload_file is not None:
        bytes_data=upload_file.getvalue()

        image_parts=[
            {
                "mime_type": upload_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
#Create a Function the get the response from Gemini LLM
def get_gemini_response(input, image, prompt):
    response=model.generate_content([input, image[0], prompt]) 
    return response.text


# creating a UI with streamlit

st.set_page_config(page_title="Food scanning system using Google gemini")
input=st.text_input("Input prompt: ", key='input')
upload_file=st.file_uploader("Choose an Image...", type=["jpg","jpeg","png"])
image=""
if upload_file is not None:
    image=Image.open(upload_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
submit=st.button("Scan the food Image and tell me the calories and others neutrients")


#Let's Create the prompt
input_prompt="""
You are an expert in indentify different types of food in images. 
The system should accurately detect and label various foods displayed in the image, providing the name 
of the food and its location within the image (e.g., bottom left, right corner, etc.). Additionally, 
the system should extract nutritional information and categorize the type of food (e.g., fruits, vegetables, grains, etc.) 
based on the detected items. The output should include a comprehensive report or display showing the
identified foods, their positions, names, and corresponding nutritional details.

"""

#Submit to Gemini Vision API:
if submit:
    image_data=input_image_details(upload_file)
    response=get_gemini_response(input_prompt, image_data,input)
    st.subheader("The Report is: ")
    st.write(response)
