import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def write(data):
	df, df_key = data
	
	st.title("Descriptive statistics 📊")
	
	########
	st.write("### Raw data statistics")
	
	st.write("This table shows the raw descriptive statistics (count, mean, standard deviation, minimum, maximum, and quartiles) of all columns in the used dataset.")
	st.write("+ Scroll to the right to see all variables.\n + Click on the column names to sort its values.")
	
	# round descriptive statistics
	variables = df_key.index[df_key["n_digits"] >= 0].tolist()
	stats = df[variables].describe()
	for var in variables:
		n = int(df_key.loc[var, "n_digits"])
		stats[var] = stats[var].round(n)
	stats = stats.astype(str)
	st.write(stats)
	
	########
	st.write("### Number of observations over time")
	st.write("Explore how many trips were recorded in the dataset per month over the entire study duration.")
	st.write("+ Play with the figure and select only a few months of interests or toggle the different modes on the right.\n + Double-click on a mode in the legend to only view this mode's counts.")
	
	fig = go.Figure()
	
	labels = df["label"].unique()
	for label in labels:
		fig.add_trace(go.Histogram(x=df.loc[df["label"]==label, "date"], name=label))
	
	fig.update_layout(xaxis_title_text="Date", yaxis_title_text="Number of observations", bargap=0.1, barmode="stack")
	fig.update_xaxes(ticklabelmode="period")
	
	st.plotly_chart(fig, sharing="streamlit")
	
	
	########
	st.write("### Explore the data with different charts")
	
	st.write("In this section, you can explore the different variables contained in the dataset using different plot types (histogram, scatter plot, or boxplot). Select the variables you're interested in to learn more about.")

	# Chart options
	options = ['Histogram', 'Scatterplot', 'Boxplot']
	chart = st.radio('Choose a chart', options)

	# Hide some warnings
	st.set_option('deprecation.showPyplotGlobalUse', False)

	if chart == 'Histogram':
		# if choose this, a column list is showed
		column = st.selectbox("Select a variable to draw a histogram for:", df.columns)
		# After the user select one, the chart is displayed
		plt.hist(df[column].values)
		st.pyplot()


	if chart == 'Scatterplot':
		# As you must know, the scatter is good to correlations
		# that's why we have two fields to select columns
		x = st.selectbox("Select a variable for the horizontal (x) axis:", df.columns)
		y = st.selectbox("Select a variable for the vertical (y) axis:", df.columns)
		
		if x and y:
			# when the columns have values we prepare 
			# the values and put on the chart
			x = df[x].values
			x = x.reshape(-1, 1)
			plt.scatter(x, df[y].values)
			st.pyplot()

	if chart == 'Boxplot':
		# Field to select multiple columns
		columns = st.multiselect("Select the variables to draw a boxplot for:", df.columns)            
		if len(columns) > 0:
			# Is there any column selected? Then the chart is plotted
			df.boxplot(column=columns)
			st.pyplot()

	
