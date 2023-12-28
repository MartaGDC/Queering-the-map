from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import nltk
nltk.download('wordnet')
nltk.download('vader_lexicon')
from nltk.corpus import stopwords
# import pymysql
# import sqlalchemy as alch
# from dotenv import load_dotenv
# import os
import random


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

# load_dotenv()
# password = os.getenv("password")
# dbName = os.getenv("dbName")
# connectionData=f"mysql+pymysql://root:{password}@localhost/{dbName}"
# engine = alch.create_engine(connectionData)

def query1(input_country, input_words):
    if input_country == "The world":
        df_query = df[df["comment"].str.lower().str.contains(f'\\b{input_words.lower()}\\b', regex=True)]
        # query = f"SELECT comment FROM queer WHERE comment REGEXP '(?i)\\\\b{input_words}\\\\b';"
    else:
        df_query = df[(df["country_name"].str.lower()==input_country.lower()) & (df["comment"].str.lower().str.contains(f'\\b{input_words.lower()}\\b', regex=True))]
        # query = f"SELECT comment FROM queer WHERE country_name = '{input_country}' AND comment REGEXP '(?i)\\\\b{input_words}\\\\b';"
    # df_query = pd.read_sql_query(query, engine)
    texts = " ".join(df_query["comment"])
    words = texts.lower().split()
    words.count(input_words)
    string_explain = f"There are a total of {df_query.shape[0]} comments with the word '{input_words}'. This word is repeated {words.count(input_words.lower())} times."
    string_comment=""
    try:
        indexes = random.choices(range(df_query.shape[0]), k=10)
        for i in indexes:
            string_comment += f"\n- {df_query['comment'].iloc[i]}\n"
        length = 10
    except:
        for i in df_query.index:
            string_comment += f"\n- {df_query['comment'].iloc[i]}\n"
        length = df_query.shape[0]
    return string_explain, string_comment, length

def query2(input_minmax, input_sentemo, inputCountry):
    if input_minmax == "Minimum":
        input_minmax = "min"
    else:
        input_minmax = "max"
    if inputCountry == "The world":
        # query = f"SELECT DISTINCT(comment) FROM queer WHERE {input_sentemo} = (SELECT {input_minmax}({input_sentemo}) FROM queer);"
        if input_minmax == "min":
            query = df[[input_sentemo.lower()]].min()[input_sentemo.lower()]
        else:
            query = df[[input_sentemo.lower()]].max()[input_sentemo.lower()]
        df_query = df[["comment"]][df[input_sentemo.lower()] == query].reset_index()
        string_comment = f"\n{df_query['comment'][0]}"
    else:
        # query = f"SELECT DISTINCT(comment) FROM queer WHERE {input_sentemo} = (SELECT {input_minmax}({input_sentemo}) FROM queer WHERE country_name= '{imputCountry}') AND country_name = '{imputCountry}';"
        if input_minmax == "min":
            query = df[[input_sentemo.lower()]].groupby(df["country_name"]).min().loc[inputCountry][input_sentemo.lower()]
        else:
            query = df[[input_sentemo.lower()]].groupby(df["country_name"]).max().loc[inputCountry][input_sentemo.lower()]
    # df_query = pd.read_sql_query(query, engine)
        df_query = df[["comment"]][(df[input_sentemo.lower()] == query) & (df["country_name"] == inputCountry)].reset_index()
        string_comment = f"\n{df_query['comment'][0]}"
    return string_comment