import streamlit as st
import pandas as pd
# import numpy as np
# import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
# import datetime as dt
# from datetime import datetime
# from pytz import timezone
# import pytz
import plotly.express as px


def write(data):
	df, df_key = data
	
	st.title("Explore mode choices 🚲🚌")

			
	#Interactive plot here distance and duration is not added
	# df1 = pd.read_csv('full_geolife+weather.csv')
	st.markdown("### Interactive Plot based on mode choice")
	st.write("+ Play with the figure and select only a subset or toggle the different modes on the right.\n + Double-click on a mode in the legend to only view this mode's counts.")
	distribution_option = ["box", "violin", "rug"]
	distribution = st.radio('Choose a distribution chart', distribution_option)
	df2=df[['Converted_Start_Hour', 'Converted_End_Hour', 'Converted_Start_Day', 'Converted_End_Day', 'temp', 'dew', 'humidity', 'precip', 'windspeed', 'cloudcover', 'visibility', 'label']]
	z = st.selectbox("Select a variable", df2.columns)
	fig = px.histogram(df2, x=z, color="label",
					   marginal=distribution, # box or violin, rug
					   hover_data=df2.columns)
	fig.update_layout(title_text='Histogram', xaxis_title=df_key.loc[z,"full_name"], height=600)
	st.plotly_chart(fig, use_container_width=True, sharing="streamlit")
