import streamlit as st
import pandas as pd

import src.home
# import src.about
import src.statistics
import src.map
import src.weather
import src.explore
# import src.model #model results can be included here in the future


st.set_page_config(
		page_title="GeoLife Mobility and Weather Data for Beijing, China",
		page_icon="🌏",
		layout="wide",
		initial_sidebar_state="expanded",
	)

PAGES = {
	"Home": src.home, 
	# "About": src.about, 
	"Descriptive statistics": src.statistics, 
	"Map the data": src.map, 
	"Explore weather conditions": src.weather, 
	"Explore mode choices": src.explore, 
	# "Model mode choices": src.model, 
}

#####

def main():
	data = get_data()
	
	# application architecture
	st.sidebar.title("GeoLife Mobility and Weather Data for Beijing, China 🌆")
	st.sidebar.subheader("Navigation")
	selection = st.sidebar.radio("Go to", list(PAGES.keys()))

	page = PAGES[selection]

	with st.spinner(f"Loading {selection} ..."):
		page.write(data)

	st.sidebar.info("**Contributors:** Steffen Coenen, Dhruvil Patel, Vaibhavi Lakshmi Segu, Ekin Uğurel")
	
	st.sidebar.info("**Full material:** The full dataset and all code is available at the corresponding [GitHub repository](https://github.com/steffen-coe/GeoLife-Mobility-Data-App).")

@st.cache(allow_output_mutation=True)
def get_data():
	# df = pd.read_csv("data/full_geolife+weather.csv")
	df = pd.read_csv("data/full_geolife+weather_dates_fmted.csv")
	
	date_columns = ["date", "Converted_TimeStart", "Converted_TimeEnd", "sunrise", "sunset"]
	for col in date_columns:
		df[col] = pd.to_datetime(df[col])
	df["sunrise"] = df["sunrise"].dt.time
	df["sunset"] = df["sunset"].dt.time
	
	df_key = pd.read_csv("data/full_geolife+weather_key.csv", index_col="column")
	
	return df, df_key

if __name__ == "__main__":
	main()



