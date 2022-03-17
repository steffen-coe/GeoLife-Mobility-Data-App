import streamlit as st
import pandas as pd
import plotly.graph_objs as go

def write(data):
	df, df_key = data
	
	st.title("Explore weather conditions 🌦️")
	
	st.write("On this page, you can explore the weather conditions in Beijing observed during the study period (from April 2007 to December 2011).")
	st.write("Go ahead and select a meteorological variable that you're interested in to learn more about.")
	st.write("+ Play with the figure and select only a few months of interests or toggle the different variables on the right.")
	
	option = st.selectbox(
		"Select weather variable:", 
		("Temperature", "Precipitation", "Wind speed", "Moon phase", "Length of day (sunrise/sunset)")
	)
	
	plot_weather_variable(data, option)


def plot_weather_variable(data, var):
	df, df_key = data
	
	# create interactive timeseries for weather data
	yss = {
			"Temperature" : ["temp", "tempmin", "tempmax", "dew"], 
			"Precipitation" : ["precip"], 
			"Wind speed" : ["windspeed"], 
			"Moon phase" : ["moonphase"], 
			"Length of day (sunrise/sunset)" : ["sunrise", "sunset"], 
	}
	
	ys = yss[var]
	
	l = []
	for y in ys:
		d = go.Scatter(
				x = df["date"],
				y = df[y],
				name = df_key.loc[y, "full_name"], 
				line = dict(color = df_key.loc[y, "color"]), 
				opacity = 0.8)
		
		l += [d]
	
	#ylabel
	ylabel = var
	unit   = df_key.at[ys[0], "unit"]
	if type(unit) == str:
		ylabel += " (%s)"%unit
	
	layout = dict(
		title = var, 
		title_x=0.5, 
		xaxis_title = "Date", 
		yaxis_title = ylabel, 
		xaxis = dict(
			rangeselector = dict(
				buttons=list([
					dict(count=1,
						 label="1m",
						 step="month",
						 stepmode="backward"),
					dict(count=6,
						 label="6m",
						 step="month",
						 stepmode="backward"),
					dict(step="all")
				])
			),
			rangeslider = dict(
				visible = True
			),
			type = "date"
		)
	)

	fig = dict(data=l, layout=layout)
	
	st.plotly_chart(fig, use_container_width=True, sharing="streamlit")
