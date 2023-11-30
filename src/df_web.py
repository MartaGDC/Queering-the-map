import json
import pandas as pd
import geopandas as gpd
from pymongo import MongoClient


def create_mongoDB(database):
    '''
    Creates a mongoDB with all the countries' polygons if it doesn't exist
    '''
    geo = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))   # GeoPandas
    geo.to_file("../data/world.geojson", driver='GeoJSON')              # Geopandas saved to geojson
    with open("../data/world.geojson") as x:
        json_countries = json.load(x)                                   # Read the geojson
    json_countries = [i for i in json_countries["features"]]            # Get a clean dictionary to be able to create a geojson
    
    client = MongoClient("localhost:27017")                             # Connect to MongoDB
    db = client.get_database(database)                                  # Get the database input in the function ("Ironhack")
    try:                                                                # If worldDB exists, get it
        db.validate_collection("worldDB")
        worldDB = db.get_collection("worldDB")
    except:                                                             # If it doesn't exist, create and fill it
        db.create_collection("worldDB")
        worldDB = db.get_collection("worldDB")
        worldDB.insert_many(json_countries)
    return worldDB                                                      # return the clean geojson


def get_df(data, worldDB):
    '''
    Latitude, longitude, comment and id_web from the data input; country from the geojson input.
    '''
    latitude = [j["latitude"] for i in data for j in i["moment_list"]]
    longitude = [j["longitude"] for i in data for j in i["moment_list"]]
    comment = [j["description"] for i in data for j in i["moment_list"]]
    id_web = [j["id"] for i in data for j in i["moment_list"]]
    dict_ = {
        "lat": latitude,
        "long": longitude,
        "comment": comment,
        "id_web": id_web
    }
    df = pd.DataFrame(dict_).sort_values("id_web").reset_index(drop=True)
    df["positions"] = df.apply(lambda row: [row["long"], row["lat"]], axis=1)
    
    country = []
    for index, rows in df.iterrows():
        try:
            country.append(worldDB.find_one({"geometry": {"$geoIntersects": {"$geometry": {'type': 'Point', 'coordinates': df["positions"][index]}}}})["properties"]["name"])
        except:
            country.append(float('nan'))
    
    codes = []
    for index, rows in df.iterrows():
        try:
            codes.append(worldDB.find_one({"geometry": {"$geoIntersects": {"$geometry": {'type': 'Point', 'coordinates': df["positions"][index]}}}})["properties"]["iso_a3"])
        except:
            codes.append(float('nan'))
    
    df["Country Name"] = country
    df["Country Code"] = codes
        
    return df


with open("../data/data_comments.json", "r") as file:
    data = json.load(file)
worldDB = create_mongoDB("Ironhack")

df = get_df(data, worldDB)
df.to_csv("../data/web")


    
    
    




