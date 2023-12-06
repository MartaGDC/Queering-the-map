from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import nltk
nltk.download('wordnet')
nltk.download('vader_lexicon')
from nltk.corpus import stopwords
import pymysql
import sqlalchemy as alch
from dotenv import load_dotenv
import os



df = pd.read_csv("data/total_df.csv", index_col="Unnamed: 0")

stop_words = set(stopwords.words("english"))

def create_wordcloud(country):
    if country == "The world":
        lines = df["comment"]
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

load_dotenv()
password = os.getenv("password")
dbName = os.getenv("dbName")
connectionData=f"mysql+pymysql://root:{password}@localhost/{dbName}"
engine = alch.create_engine(connectionData)

def query1(input_country, input_words):
    if input_country == "The world":
        query = f"SELECT comment FROM queer WHERE comment REGEXP '(?i)\\\\b{input_words}\\\\b';"
    else:
        query = f"SELECT comment FROM queer WHERE country_name = '{input_country}' AND comment REGEXP '(?i)\\\\b{input_words}\\\\b';"
    df_query = pd.read_sql_query(query, engine)
    texts = " ".join(df_query["comment"])
    words = texts.split()
    words.count(input_words)
    string_explain = f"There are a total of {df_query.shape[0]} comment in {input_country} with the word '{input_words}'. This words is repeated {words.count(input_words)} times."
    if df_query.shape[0] > 250:
        string_comment = "That's a lot. I know that you are very curious, so if you want to see any comments, try with another country or another words :wink:"
    else:
        string_comment = ""
        for i in df_query.index:
            string_comment += f"{i+1}. {df_query['comment'][i]}\n"
    return string_explain, string_comment

def query2(input_minmax, input_sentemo, imputCountry):
    if input_minmax == "Minimum":
        input_minmax = "MIN"
    else:
        input_minmax = "MAX"
    if imputCountry == "The world":
        query = f"SELECT DISTINCT(comment) FROM queer WHERE {input_sentemo} = (SELECT {input_minmax}({input_sentemo}) FROM queer);"
    else:
        query = f"SELECT DISTINCT(comment) FROM queer WHERE {input_sentemo} = (SELECT {input_minmax}({input_sentemo}) FROM queer WHERE country_name= '{imputCountry}') AND country_name = '{imputCountry}';"
    df_query = pd.read_sql_query(query, engine)
    string_comment = f"\n{df_query['comment'][0]}"
    return string_comment