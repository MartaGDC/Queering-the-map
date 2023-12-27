import streamlit as st
import base64


# In every page I will set a different page_title with a new icon, while in this first I will do a couple of different things:
# Apart from the text, you can add emojis between ":". The complete list is here: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
st.set_page_config(
     page_title="Ironhacking the queer map",
     page_icon=":rainbow:",
     layout="wide",
     initial_sidebar_state="expanded"
 )

st.title("Ironhacking the queer map")

st.markdown(
    """
    <style>
        .stMarkdown h2 {text-align: center;}
        .centered-link {text-align: center;}  
    </style>
    """,
    unsafe_allow_html=True)

enlace_url = 'https://www.queeringthemap.com/'

main_content = f"<h2> The Map </h2> <div class='centered-link'><a href='{enlace_url}'>www.queeringthemap.com</a></div><h1>  </h1>"
st.markdown(main_content, unsafe_allow_html=True) # The web cannot be embeded in streamlit because of security issues

explanation_content = f"In 2017, the webpage Queeringthemap.com was created for sharing stories and experiences lived by queer people in order to protect and keep their voices. This page is for presenting the result of my final project in Ironhack Data Analysis Bootcamp: the analysis of the discourse in this page.<h1>  </h1>"
st.markdown(explanation_content, unsafe_allow_html=True)
 
map_image = "images/map_frontpage.png"
with open(map_image, "rb") as img_file:
    map_image_base64 = base64.b64encode(img_file.read()).decode()
    
# Generar el código HTML para la imagen con el enlace
codigo_map = f'<a href="{enlace_url}" target="_blank"><img style="width: 100%;" src="data:image/png;base64,{map_image_base64}" alt= "Image not found"></a>'
st.markdown(codigo_map, unsafe_allow_html=True)