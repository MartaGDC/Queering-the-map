import pandas as pd
import numpy as np
import langid
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def detect_language(text):
    return langid.classify(text)[0]

def sentiment (x):
    sia = SentimentIntensityAnalyzer()
    try:
        return sia.polarity_scores(x)["compound"]
    except:
        return float('nan')
    
def type_sentiment(x):
    if x < 0:
        return "neg"
    elif x > 0:
        return "pos"
    else:
        return "neu"

def number_char(x):
    return len(x)

def get_emotionality(df):
    max_length = df["characters"].max()
    length_standard = [(rows["characters"] / max_length) for index, rows in df.iterrows()]
    emotionality = ((abs(df["sentiment"])) + 1) * length_standard
    return emotionality

def get_total_csv(path1, path2, name):
    discourse = pd.read_csv(path1, index_col="Unnamed: 0") # "../data/web.csv"
    discourse["language_langid"] = discourse["comment"].apply(detect_language)
    discourse["sentiment"] = discourse["comment"].apply(sentiment)
    discourse["type_sentiment"] = discourse["sentiment"].apply(type_sentiment)
    discourse["characters"] = discourse["comment"].apply(number_char)
    discourse = discourse.loc[(discourse["characters"] != discourse["characters"].max())]
    discourse = discourse.loc[(discourse["characters"] != discourse["characters"].min())]
    discourse["emotionality"] = get_emotionality(discourse)
    discourse.loc[discourse[discourse["Country Code"]=="-99"].index, "Country Code"] = "XXK"
    
    features = pd.read_csv(path2, index_col="Unnamed: 0") # "../data/charactCountry/country_features.csv"
    df = discourse.merge(features, how="left", on= "Country Code")
    
    df = df[["id_web", "lat", "long", "comment", "language_langid", "sentiment", "type_sentiment", "characters", "emotionality", 
        'Country Name_x', 'Country Code', 'Region', 'IncomeGroup','mean_stability', 'mean_law', 'mean_female_seats',
        'mean_voice', 'mean_gdp', 'mean_children_out', 'mean_ed_exp', 'mean_literacy', 'mean_ARV_coverage', 'mean_health_exp',
        'mean_UHC_coverage', 'mean_rights', 'mean_sex_index', 'censor', 'transition', 'mean_hate_protection']]
    df.rename(columns={"language_langid": "language", "Country Name_x": "country_name", "Country Code": "country_code",
                   "Region": "region", "IncomeGroup": "income_group"}, inplace = True)
    
    df.to_csv(f"../data/{name}.csv") # "total_df"


get_total_csv("../data/web.csv", "../data/charactCountry/country_features.csv", "total_df")
