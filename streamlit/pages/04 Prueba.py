import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd

# Datos de ejemplo: Puedes reemplazar esto con tus propios datos
data = {'Country': ['USA', 'Canada', 'Mexico', 'Brazil', 'Argentina'],
        'Latitude': [37.7749, 56.1304, 23.6345, -14.2350, -38.4161],
        'Longitude': [-122.4194, -106.3468, -102.5528, -51.9253, -63.6167]}

df = pd.DataFrame(data)

# Streamlit
st.title('Mapa interactivo con botones por país')

# Crear un mapa folium
m = folium.Map(location=[0, 0], zoom_start=2)

# Agregar botones por país
for i, row in df.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']],
                  popup=row['Country'],
                  tooltip=row['Country'],
                  icon=folium.Icon(color='blue')).add_to(m)

# Mostrar el mapa interactivo en Streamlit
folium_static(m)