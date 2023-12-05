import streamlit as st
import pandas as pd
import numpy as np


df = pd.read_csv("data/total_df.csv")
countries = df["country_name"].unique()
countries = np.insert(countries, 0, "The world") # By default, the total comments


st.set_page_config(page_title="Content", page_icon=":bulb:", layout="wide")

st.title("What would you like to know")

st.write("**Select a country**")

selected_country = st.selectbox(" ", countries)
