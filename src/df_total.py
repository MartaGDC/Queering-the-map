import pandas as pd
import numpy as np
import langid
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.cluster import KMeans


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
        return 1
    elif x == 0:
        return 2
    else:
        return 3

def number_char(x):
    return len(x)

def get_emotionality(df):
    max_length = df["characters"].max()
    length_standard = [(rows["characters"] / max_length) for index, rows in df.iterrows()]
    emotionality = ((abs(df["sentiment"])) + 1) * length_standard
    return emotionality

def get_total_csv(path1, path2, name):
    discourse = pd.read_csv(path1, index_col="Unnamed: 0")
    discourse["language_langid"] = discourse["comment"].apply(detect_language)
    discourse["sentiment"] = discourse["comment"].apply(sentiment)
    discourse["type_sentiment"] = discourse["sentiment"].apply(type_sentiment)
    discourse["characters"] = discourse["comment"].apply(number_char)
    discourse = discourse.loc[(discourse["characters"] != discourse["characters"].max())]
    discourse = discourse.loc[(discourse["characters"] != discourse["characters"].min())]
    discourse["emotionality"] = get_emotionality(discourse)
    discourse.loc[discourse[discourse["Country Code"]=="-99"].index, "Country Code"] = "XXK"
    
    features = pd.read_csv(path2, index_col="Unnamed: 0")
    df = discourse.merge(features, how="left", on= "Country Code")
    
    df = df[["id_web", "lat", "long", "comment", "language_langid", "sentiment", "type_sentiment", "characters", "emotionality", 
        'Country Name_x', 'Country Code', 'Region', 'IncomeGroup','mean_stability', 'mean_law', 'mean_female_seats',
        'mean_voice', 'mean_gdp', 'mean_children_out', 'mean_ed_exp', 'mean_literacy', 'mean_ARV_coverage', 'mean_health_exp',
        'mean_UHC_coverage', 'mean_rights', 'mean_sex_index', 'censor', 'transition', 'mean_hate_protection']]
    df.rename(columns={"language_langid": "language", "Country Name_x": "country_name", "Country Code": "country_code",
                   "Region": "region", "IncomeGroup": "income_group"}, inplace = True)
    
    df_copy = df[["lat", "long", "country_code"]]
    countries = list(set(df["country_code"])) 
    for i in countries:
        try:
            km = KMeans(n_clusters=6, n_init=10)
            km.fit(df_copy[["lat", "long"]][df_copy["country_code"]==i])
            cluster_pred = km.predict(df_copy[["lat", "long"]])
            df_copy[i] = cluster_pred
        except:
            try:
                km = KMeans(n_clusters=5, n_init=10)
                km.fit(df_copy[["lat", "long"]][df_copy["country_code"]==i])
                cluster_pred = km.predict(df_copy[["lat", "long"]])
                df_copy[i] = cluster_pred
            except:
                try:
                    km = KMeans(n_clusters=4, n_init=10)
                    km.fit(df_copy[["lat", "long"]][df_copy["country_code"]==i])
                    cluster_pred = km.predict(df_copy[["lat", "long"]])
                    df_copy[i] = cluster_pred
                except:
                    try:
                        km = KMeans(n_clusters=3, n_init=10)
                        km.fit(df_copy[["lat", "long"]][df_copy["country_code"]==i])
                        cluster_pred = km.predict(df_copy[["lat", "long"]])
                        df_copy[i] = cluster_pred
                    except:
                        try:
                            km = KMeans(n_clusters=2, n_init=10)
                            km.fit(df_copy[["lat", "long"]][df_copy["country_code"]==i])
                            cluster_pred = km.predict(df_copy[["lat", "long"]])
                            df_copy[i] = cluster_pred
                        except:
                            df_copy[i] = 0
    for i in countries:
        for j in df_copy.columns:
            if i == j:
                df_copy.loc[df_copy[df_copy["country_code"]==i].index, "cluster"] = df_copy[i]   
    
    df["cluster"] = df_copy["cluster"]
        
    df.to_csv(f"data/{name}.csv")