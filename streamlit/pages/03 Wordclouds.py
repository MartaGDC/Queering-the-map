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
import src.words_queries as words;

df = pd.read_csv("data/total_df.csv")


st.set_page_config(page_title="WordCloud", page_icon=":cloud:", layout="wide")

st.title("Word Cloud Generator")

st.header("Select a country")

countries = df["country_name"].unique()
countries = np.insert(countries, 0, "The world") # By default, the total comments
selected_country = st.selectbox(" ", countries)

# Call a function to create wordcloud and table 
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(words.create_wordcloud(selected_country))
# Call a function to create a table with top words:
table = words.create_topWords(selected_country)


col1, col2 = st.columns([1, 3]) # Wider columns for wordclouds
col1.subheader("**Word**")
col1.dataframe(table, use_container_width=False)
col2.subheader("**Clouds**")
col2.image(wordcloud.to_array(), use_column_width=True)
