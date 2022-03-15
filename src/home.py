import streamlit as st
import pandas as pd

def write(data):
	df, df_key = data
	
	st.title("Data Visualization Tool using the GeoLife Mobility and Weather Data for Beijing, China 🌆")
	
	st.write("This website is a Python-based application utilizing Streamlit to provide structured, interactive visualizations on the [GeoLife GPS Trajectories dataset](https://www.microsoft.com/en-us/download/details.aspx?id=52367&from=https%3A%2F%2Fresearch.microsoft.com%2Fen-us%2Fdownloads%2Fb16d359d-d164-469e-9fd4-daa38f2b2e13%2F).")
	
	st.write("Geolife Trajectory data set was recorded between April 2007 and December 2011. It contains information of 3 entities \n + GPS Observation \n + Ground Truth \n + Trips \n Along with these entities, we connected a Weather entity set to understand the mode choice based on the different weather conditions and other factors.")
	
	st.write("Have fun exploring the data! 💡")
	
	video_file = open('img/demo.webm', 'rb')
	video_bytes = video_file.read()
	
	st.write("**Demonstration video of this app:**")
	st.video(video_bytes)	
