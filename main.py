import json
import pandas as pd
import src.json_web as json_web
import src.df_web as web
import src.df_features as features
from src.df_features import (list_paths_WB, column_names)
import src.df_total as total
import src.discourse_viz as vis


# Get jsons from the web:
i = 1
url = "https://www.queeringthemap.com/moments.msgpack"
data = json_web.get_jsons(i, url)
with open("data/data_comments.json", "w") as file:
    json.dump(data, file)

# Get a df with the data obtained from the web
    # First get the geodata for each country (only needed to be done once). If this db already exists, it doesn't do anything
with open("data/data_comments.json", "r") as file:
    data = json.load(file)    
worldDB = web.create_mongoDB("Ironhack")
    # df
df = web.get_df(data, worldDB, "web")

# Get df with info from countries
country_income = features.get_income("data/charactCountry/stability/Metadata_Country.csv")
df = features.get_WB_features(list_paths_WB, pd.DataFrame(), column_names, country_income)
df1 = features.get_rights("data/charactCountry/equality/lgbt_rights_index.csv", df)
df2 = features.get_sex_illegal("data/charactCountry/equality/sex_illegal.csv", df1)
df3 = features.get_censor("data/charactCountry/equality/censorship.csv", df2)
df4 = features.get_trans_marker("data/charactCountry/equality/transitions.csv", df3)
df5 = features.get_hate_protection("data/charactCountry/equality/hate_protection.csv", df4)
df5 = features.preimpute_features(df5)
features.get_features_csv(df5, "country_features")

# Get final df
total.get_total_csv("data/web.csv", "data/charactCountry/country_features.csv", "total_df")

# Get grpahs
vis.graph_web_use()
vis.graph_language()
vis.graphs_sentiment()
vis.graphs_characters()
vis.graphs_emotionality()
vis.wordCloud_world()
