
# currentWorkingDirectory = "C:\\(...)\\Lec7_ Geo-Prediction"
# currentWorkingDirectory = "C:\\1 - eigenes\\Lehrauftrag - BHT\\Vorlesungsreihe WS24-25\\src_project"
# Docker:
currentWorkingDirectory = "/mount/src/berlingeoheatmap1/"

# -----------------------------------------------------------------------------
import os
os.chdir(currentWorkingDirectory)
print("Current working directory\n" + os.getcwd())

import pandas                        as pd
from core import HelperTools as ht

# -----------------------------------------------------------------------------
from core import methods                  as m1

# -----------------------------------------------------------------------------
import geopandas                     as gpd
# from shapely                         import wkt

# -----------------------------------------------------------------------------

import folium
from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import folium_static
from branca.colormap import LinearColormap

# -----------------------------------------------------------------------------
from config                          import pdict

# -----------------------------------------------------------------------------
# @ht.timer
# def main():
#     """Main: Geo-Prediction of new customers' based on calculated geo-segments"""


df_geodat_plz   = pd.read_csv("datasets/" + pdict["file_geodat_plz"],    sep=";", decimal=".")
df_geodat_dis   = pd.read_csv("datasets/" + pdict["file_geodat_dis"],    sep=";", decimal=".")

df_lstat        = pd.read_csv("datasets/" + pdict["file_lstations"],      sep=";", decimal=",")
df_lstat2       = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)
gdf_lstat3       = m1.count_plz_occurrences(df_lstat2)


df_buildings    = gpd.read_file("datasets/geb/gebaeude.shp")    #= pd.read_csv("datasets/" + pdict["file_buildings"],      sep=",", decimal=",")
df_buildings2   = m1.preprop_geb(df_buildings, pdict)                          # Data Quality Inssues


df_residents    = pd.read_csv("datasets/" + pdict["file_residents"],      sep=",", decimal=".") 
gdf_residents2   = m1.preprop_resid(df_residents, df_geodat_plz, pdict)

# df_amounttraf = pd.read_csv("datasets/" + pdict["file_amounttraf"],     sep=";", decimal=",") 

# -----------------------------------------------------------------------------------------------------------------------

# # @st.cache_data
# def display_geoheatmap_with_layers(dfr1, dfr2, pdict):
#     dframe1 = dfr1.copy()
#     dframe2 = dfr2.copy()

dframe1 = gdf_lstat3.copy()
dframe2 = gdf_residents2.copy()


# Streamlit app
st.title('Heatmaps: Electric Charging Stations and Residents')

# Create a radio button for layer selection
# layer_selection = st.radio("Select Layer", ("Number of Residents per PLZ (Postal code)", "Number of Charging Stations per PLZ (Postal code)"))

layer_selection = st.radio("Select Layer", ("Residents", "Charging_Stations"))

# Create a Folium map
m = folium.Map(location=[52.52, 13.40], zoom_start=10)

if layer_selection == "Residents":
    
    # Create a color map for Residents
    color_map = LinearColormap(colors=['yellow', 'red'], vmin=dframe2['Einwohner'].min(), vmax=dframe2['Einwohner'].max())

    # Add polygons to the map for Residents
    for idx, row in dframe2.iterrows():
        folium.GeoJson(
            row['geometry'],
            style_function=lambda x, color=color_map(row['Einwohner']): {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            },
            tooltip=f"PLZ: {row['PLZ']}, Einwohner: {row['Einwohner']}"
        ).add_to(m)
    
    # Display the dataframe for Residents
    # st.subheader('Residents Data')
    # st.dataframe(gdf_residents2)

else:
    # Create a color map for Numbers

    color_map = LinearColormap(colors=['yellow', 'red'], vmin=dframe1['Number'].min(), vmax=dframe1['Number'].max())

# Add polygons to the map for Numbers
    for idx, row in dframe1.iterrows():
        folium.GeoJson(
            row['geometry'],
            style_function=lambda x, color=color_map(row['Number']): {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            },
            tooltip=f"PLZ: {row['PLZ']}, Number: {row['Number']}"
        ).add_to(m)

    # Display the dataframe for Numbers
    # st.subheader('Numbers Data')
    # st.dataframe(gdf_lstat3)

# Add color map to the map
color_map.add_to(m)

# Display the map in Streamlit
folium_static(m, width=800, height=600)
    



# display_geoheatmap_with_layers(gdf_lstat3, gdf_residents2, pdict)

