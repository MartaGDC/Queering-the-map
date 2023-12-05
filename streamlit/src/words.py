from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import nltk
nltk.download('wordnet')
nltk.download('vader_lexicon')
from nltk.corpus import stopwords

df = pd.read_csv("data/total_df.csv")    
stop_words = set(stopwords.words("english"))

def create_wordcloud(country):
    if country == "The world":
        lines = df["comment"][df["language"]=="en"]
    else:
        lines = df[(df["country_name"] == country) & (df["language"]=="en")]["comment"]
    text = " ".join(lines)
    return text

def create_topWords(country):
    if country == "The world":
        df_words = df[df["language"]=="en"]
    else:
        df_words = df[(df["language"]=="en") & (df["country_name"]==country)]
    text = []
    for index, rows in df_words.iterrows():
        dirty_text = "".join(rows["comment"])
        words = dirty_text.split()
        for i in words:
            if i.lower() not in stop_words:
                text.append(i)
    df_text = pd.DataFrame(pd.Series(text).value_counts()).reset_index().head(10).rename(columns={"index":"Top words", "count": ""}).set_index("Top words")
    return df_text
