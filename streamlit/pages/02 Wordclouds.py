import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('wordnet')
nltk.download('vader_lexicon')
import src.words_queries as words

df = pd.read_csv("data/total_df.csv", index_col="Unnamed: 0")


st.set_page_config(page_title="WordCloud", page_icon=":cloud:", layout="wide")

st.title("WordClouds")
st.write("**Select a location to see which were the most repeated words**")
paragraph = "<h1> </h1>"
st.markdown(paragraph, unsafe_allow_html=True)

countries = df["country_name"].unique()
countries = np.insert(countries, 0, "The world")
countries = np.insert(countries, 0, "")
selected_country = st.selectbox("**Select a country**", countries)

col1, col2 = st.columns([1, 3]) # Wider columns for wordclouds
# Call a function to create wordcloud and table
if selected_country != "":
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(words.create_wordcloud(selected_country))
    table = words.create_topWords(selected_country)
    col1.subheader("**Word**")
    col1.dataframe(table, use_container_width=False)
    col2.subheader("**Clouds**")
    col2.image(wordcloud.to_array(), use_column_width=True)
else:
    pass



