import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


def write(data):
	df, df_key = data
	
	st.title("Explore mode choices 🚲🚌")
	
	st.write("On this page, in-depth visualizations of the different chosen transportation modes by the users contained in the dataset can be explored. Select different variables that you're interested in and explore how they influence the prevalence of certain mode choices, such as biking, driving, or taking the bus.")

			
	# Interactive plot
	st.markdown("### Histograms of mode choices by different variables")
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
	
	########
	st.write("### Key trip characteristics by mode choice")
	st.write("Explore the figure below to see how key trip characteristics like average speed or trip duration differ by the chosen mode. Zoom in to compare the modes in detail!")
	
	variables = ["distanceTotal", "time_total", "vel_avg", "vel_max", "vcr", "sr", "hcr"]
	options = [df_key.loc[var, "full_name"] for var in variables]
	
	s = "**Possible variables to choose from:**\n"
	for i in variables:
		s += "+ *" + df_key.loc[i, "full_name"] + "*: " + df_key.at[i, "description"] + "\n"
	st.write(s)
	
	option = st.selectbox("Select trip variable:", options)
	
	var = df_key.index[df_key["full_name"] == option].to_list()[0]
	
	#ylabel
	ylabel = option
	unit   = df_key.at[var, "unit"]
	if type(unit) == str:
		ylabel += " (%s)"%unit
	
	#boxplots by mode (using matplotlib)
	# fig, ax = plt.subplots()
	# df.boxplot(column=var, by="label", ax=ax)
	# ax.set_xlabel("Mode choice")
	# ax.set_ylabel(ylabel)
	# st.pyplot(fig)
	
	#boxplots by mode (using plotly)
	fig = px.box(df, x="label", y=var)
	fig.update_layout(xaxis_title_text="Mode choice", yaxis_title_text=ylabel)
	st.plotly_chart(fig, sharing="streamlit")
	
	
