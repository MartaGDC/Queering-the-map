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

df = pd.read_csv("data/total_df.csv")

st.set_page_config(page_title="WordCloud", page_icon=":cloud:", layout="wide")

st.title("Word Cloud Generator")

st.header("Select a country")

countries = df["country_name"].unique()
countries=np.insert(countries, 0, "The world")
selected_country = st.selectbox(" ", countries)

if selected_country == "The world":
    lines = df["comment"]
else:
    lines = df[df["country_name"] == selected_country]["comment"]

text = " ".join(lines)

# Create a WordCloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

st.image(wordcloud.to_array(), use_column_width=True)