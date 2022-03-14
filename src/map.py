import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import numpy as np

def write(data):
	df, df_key = data
	
	st.title("Map the data 🗺️")

	df = pd.DataFrame(data=df, columns=['date', 'latitudeStart', 'longitudeStart', 'latitudeEnd', 'longitudeEnd', 'label', 'temp'])
	df = df.rename(columns={'latitudeStart': 'lat', 'longitudeStart': 'lon'})

	st.write("On this page, you can visualize the data on maps.")

	# Calculate the timerange for the slider
	min_date = datetime.strptime(min(df["date"].astype("string")),"%Y-%m-%d") #.strftime('%Y-%m-%d')
	max_date = datetime.strptime(max(df["date"].astype("string")),"%Y-%m-%d") #.strftime('%Y-%m-%d')

	st.sidebar.subheader("Inputs")
	min_selection, max_selection = st.sidebar.slider(
		"Select date range", min_value=min_date, max_value=max_date, value=[min_date, max_date]
	)

	df = df[
		(df["date"] >= min_selection) & (df["date"] <= max_selection)
	]
	s = f"+ Filtering between {min_selection.date()} and {max_selection.date()}"
	s += f" ({len(df)} data points)"
	st.write(s)
	
	st.write("### Map of all start and end points of trips")

	st.map(df)
	
	st.write("### Heatmaps")
	
	st.write("Select a mode and a temperature range and observe how the distribution of start and end points on the maps below changes.")

	modes = list(df['label'].drop_duplicates())
	mode_choice = st.selectbox('Select mode:', modes)
	m = df.loc[(df['label']==mode_choice)]# & (data['temp_bins'].astype(str)==tempRange)]

	bins = [-np.inf, 0, 10, 20, 30, np.inf]
	m['temp_bins'] = pd.cut(m['temp'], bins)

	tempRange = m['temp_bins'].astype(str).unique()
	temp_choice = st.selectbox('Select temperature range:', tempRange)

	m = m.loc[m['temp_bins'].astype(str) == temp_choice]
	
	# if show_heatmap:
	x = 400
	map_heatmap_start = folium.Map(location=(39.9042, 116.4074), height=x, width="55%")
	map_heatmap_end = folium.Map(location=(39.9042, 116.4074), height=x, width="55%")
	
	# Filter the DF for columns, then remove NaNs
	heat_df_start = m[["lat", "lon"]]
	heat_df_start = heat_df_start.dropna(axis=0, subset=["lat", "lon"])
	heat_df_end = m[["latitudeEnd", "longitudeEnd"]]
	heat_df_end = heat_df_end.dropna(axis=0, subset=["latitudeEnd", "longitudeEnd"])
	
	# List comprehension to make list of lists
	heat_data_s = [
		[row["lat"], row["lon"]] for index, row in heat_df_start.iterrows()
	]
	heat_data_e = [
		[row["latitudeEnd"], row["longitudeEnd"]] for index, row in heat_df_end.iterrows()
	]
	# Plot it on the map
	HeatMap(heat_data_s).add_to(map_heatmap_start)
	HeatMap(heat_data_e).add_to(map_heatmap_end)
	# Display the map using the community component
	
	s = f"+ Filtering between {min_selection.date()} and {max_selection.date()}"
	s += f" ({len(df)} data points)"
	st.write(s)
	
	
	col1, col2 = st.columns(2)
	with col1:
		st.subheader("Trip start locations")
		folium_static(map_heatmap_start)
	with col2:
		st.subheader("Trip end locations")
		folium_static(map_heatmap_end)
		
	# if show_mode:
	ms_coords = pd.DataFrame(data=m, columns=("lat", "lon"))
	me_coords = pd.DataFrame(data=m, columns=("latitudeEnd", "longitudeEnd"))
	
	mode_map = folium.Map(location=(39.9042, 116.4074))
	
	for i in range(0,len(ms_coords)):
		folium.Circle(location=[ms_coords.iloc[i]['lat'],ms_coords.iloc[i]['lon']], color='red').add_to(mode_map)
	
	for i in range(0,len(ms_coords)):
		folium.Circle(location=[me_coords.iloc[i]['latitudeEnd'],me_coords.iloc[i]['longitudeEnd']], color='blue').add_to(mode_map)

	# st.subheader("Trip Start/End Points by Mode and Temperature")
	# st.write(f"Filtering between {min_selection.date()} & {max_selection.date()}")
	# st.write(f"Data Points: {len(m)}")
	st.write("Individual start and end points:")
	st.write("**Legend:**")
	legend = pd.DataFrame({'Trip Start Point': ['Red'], 'Trip End Point': ['Blue']})
	st.table(legend.style.hide_index())
	folium_static(mode_map)
