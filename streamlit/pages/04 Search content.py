import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import src.words_queries as words

df = pd.read_csv("data/total_df.csv", index_col="Unnamed: 0")
countries = df["country_name"].unique()
countries = np.insert(countries, 0, "The world") # By default, the total comments


st.set_page_config(page_title="Content", page_icon=":bulb:", layout="wide")

st.title("Who said what?")
st.write("**Select a country and a text to know how many times it was repeated and which are the experiences shared**")

col1, col2 = st.columns([1, 1])

paragraph = "<h1> </h1>"
col1.markdown(paragraph, unsafe_allow_html=True)
selected_country = col1.selectbox("**Select a country**", countries, key="1")
input_word = col1.text_input(label = "**Choose a word**")

image1 = Image.open("images/world_pride.png")
col2.image(image1, use_column_width=True)

# Call a function to make the query
yesno = ["", "Yes", "No"]

string_explain, string_comment, length = words.query1(selected_country, input_word)
if input_word != "":
    st.write(string_explain)
    if length == 10:
        st.write("That's a lot. Do you want to see a random sample of 10 of these comments?")
        select_show = st.selectbox("Yes/No", yesno)
        if select_show == "Yes":
            st.write(string_comment)
        else:
            pass
    elif length > 0:
        st.write("Do you want to see these comments?")
        select_show = st.selectbox("Yes/No", yesno)
        if select_show == "Yes":
            st.write(string_comment)
        else:
            pass
    else:
        pass


st.title("Emotionality and sentiment of the shared experiences")
st.write("**See the comment with the most intense or numb feelings within a country**")


col3, col4, col5 = st.columns([1, 1, 1])

paragraph = "<h1> </h1>"
col3.markdown(paragraph, unsafe_allow_html=True)
minmax = ["", "Minimum", "Maximum"]
emotion = ["", "Sentiment", "Emotionality"]
input_minmax = col3.selectbox("**Select minimum or maximum**", minmax)
input_emotion = col3.selectbox("**Select what you want to explore**", emotion)
input_country = col3.selectbox("**Select a country**", countries, key="2")

image2 = Image.open("images/emotions.png")
col5.image(image2, use_column_width=True)


# Call a function to make the query
if input_minmax == "" or input_emotion == "":
    pass
else:
    string_other_comment = words.query2(input_minmax, input_emotion, input_country)
    st.write(string_other_comment)