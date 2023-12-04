import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import numpy as np
from wordcloud import WordCloud

st.set_page_config(
     page_title="Prueba",
     layout="wide"
     )

# Datos de ejemplo: Puedes reemplazar esto con tus propios datos
df = pd.read_csv("../data/total_df.csv", index_col="Unnamed: 0")
data = df.groupby("country_name").agg({"lat": "median", "long":"median"}).reset_index()
# Streamlit
st.title('Mapa interactivo con botones por país')

map = folium.Map(location=[0, 0], zoom_start=2, width="100%")

def generate_wordcloud(comments):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    st.image(wordcloud.to_image())

def on_marker_click(e):
    country_name = e.target.options.tooltip
    if country_name == None:
        lines = df['comment']
    else:
        lines = df[data['country_name'] == country_name]['comment']
    text = " ".join(lines)
    generate_wordcloud(text)





# Manejar el evento en Streamlit
if st.session_state.marker_button_clicked:
    st.write("¡Se hizo clic en el marcador!")
    
    
    



# Agregar el código JavaScript al mapa
map.get_root().script.add_child(folium.Element(js_code))


for i, row in data.iterrows():
    folium.Marker([row['lat'], row['long']],
                  tooltip=row['country_name'],
                  icon=folium.Icon(color='blue'),
                  popup="<a href='#' id='marker_button'></a>").add_to(map)

folium_static(map)

# Agregar un manejador de eventos en JavaScript para el clic en el enlace
st.script("""
document.getElementById('marker_button').addEventListener('click', function() {
    Streamlit.setComponentValue('marker_button_clicked', true);
});
""")


