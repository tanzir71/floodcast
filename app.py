import streamlit as st
import pandas as pd
import datetime
import altair as alt

# Set the page configuration
st.set_page_config(
    page_title="FloodCast - Bangladesh Rainfall Monitoring",  # Set your desired page title
    page_icon="🌊",                # Optional: Set a favicon
    layout="centered",                 # Optional: Set the layout (centered or wide)
)

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv('monthly_rainfall.csv')

df = load_data()

month_mapping = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

# Set to previous month
current_month = datetime.datetime.now().month

if current_month == 1:
    previous_month = month_mapping[12]
else:
    previous_month = month_mapping[current_month - 1]

# Set the title for the app
st.title('Past Rainfall in ' + previous_month)

# Map the month names in the DataFrame
df['Month'] = df['Month'].map(month_mapping)
df['Year'] = df['Year'].map('{:}'.format)

# Select the month for the bar chart
selected_month = st.selectbox('Select Month:', df['Month'].unique(), index=list(df['Month'].unique()).index(previous_month))

# Filter the data for the selected month
filtered_df = df[df['Month'] == selected_month]

# Group by station and find the maximum rainfall for each station
max_rainfall = filtered_df.groupby('Station')['Rainfall'].max().reset_index()

# Find the station with the highest rainfall
station_with_max_rainfall = max_rainfall.loc[max_rainfall['Rainfall'].idxmax()]

# Create a bar chart to display the maximum rainfall for each station using Altair
bar_chart = alt.Chart(max_rainfall).mark_bar().encode(
    x='Station',
    y='Rainfall',
    color=alt.condition(
        alt.datum.Station == station_with_max_rainfall['Station'],  # Highlight the max rainfall station
        alt.value('red'),  # Color for the highest rainfall station
        alt.value('steelblue')  # Default color for other stations
    )
).properties(
    title='Maximum Rainfall by Station'
)

# Display the bar chart
st.altair_chart(bar_chart, use_container_width=True)

# Set the default selected location to the station with the highest rainfall
selected_location = st.selectbox('Select Location:', filtered_df['Station'].unique(), index=list(filtered_df['Station'].unique()).index(station_with_max_rainfall['Station']))

# Filter the data for the selected location
filtered_data = filtered_df[filtered_df['Station'] == selected_location]

# Sort the data by 'Rainfall' in descending order
filtered_data = filtered_data.sort_values(by='Rainfall', ascending=False)

# Display the dataframe without row numbers and index
filtered_data.reset_index(drop=True, inplace=True)

# Highlight the row with the highest rainfall
max_rainfall_row = filtered_data.iloc[0]
filtered_data = filtered_data.style.apply(lambda x: ['background: red' if x.name == max_rainfall_row.name else '' for _ in x], axis=1)

# Display the dataframe without row numbers
st.subheader(f"Rainfall Data for {selected_month} at {selected_location}")
st.table(filtered_data)