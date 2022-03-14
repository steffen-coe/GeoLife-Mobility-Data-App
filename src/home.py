import streamlit as st
import pandas as pd

def write(data):
	df, df_key = data
	
	st.title("Data Visualization Tool using the GeoLife Mobility and Weather Data for Beijing, China 🌆")
	
	st.write("A Python-based application utilizing Streamlit to provide structured, interactive visualizations on the [GeoLife GPS Trajectories dataset](https://www.microsoft.com/en-us/download/details.aspx?id=52367&from=https%3A%2F%2Fresearch.microsoft.com%2Fen-us%2Fdownloads%2Fb16d359d-d164-469e-9fd4-daa38f2b2e13%2F).")
	
	st.write("Geolife Trajectory data set contains information of 3 entities \n + GPS Observation \n + Ground Truth \n + Trips \n Along with these entities, the Weather entity is connected to understand the mode choice based on the different weather conditions and other factors.")
	
	#TODO: include some basic model outcomes (incl. odds ratios)
	
