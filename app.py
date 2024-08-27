import streamlit as st
import pandas as pd
import datetime
import altair as alt

# Set the page configuration
st.set_page_config(
    page_title="FloodCast - Bangladesh Rainfall Monitoring",  # Set your desired page title
    page_icon="🌊",                # Optional: Set a favicon
    layout="centered",             # Optional: Set the layout (centered or wide)
)

st.header("FloodCast — Bangladesh Rainfall Monitoring")
st.markdown("This app provides real-time rainfall data for Bangladesh, including historical rainfall data and latest rainfall data. It also provides water levels data, which is used to highlight areas with water levels that are at least a specified percentage of the danger level.")
st.divider()

# Load the CSV files
@st.cache_data
def load_data():
    monthly_df = pd.read_csv('monthly_rainfall.csv')
    return monthly_df

@st.cache_data  
def load_latest_data():
    latest_df = pd.read_csv('latest_rainfall.csv')
    return latest_df

# Load water levels data
@st.cache_data
def load_water_levels():
    water_levels_df = pd.read_csv('water_levels.csv')
    
    # Convert 'WL Observed' and 'Danger Level' to numeric, coercing errors
    water_levels_df['WL Observed'] = pd.to_numeric(water_levels_df['WL Observed'], errors='coerce')
    water_levels_df['Danger Level'] = pd.to_numeric(water_levels_df['Danger Level'], errors='coerce')
    
    return water_levels_df

water_levels_df = load_water_levels()
df = load_data()
latest_df = load_latest_data()

# Ensure the 'Rainfall' columns are numeric
df['Rainfall'] = pd.to_numeric(df['Rainfall'], errors='coerce')
latest_df['Cumulative'] = pd.to_numeric(latest_df['Cumulative'], errors='coerce')

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
st.subheader('⌛ Historical Rainfall')
st.markdown('The maximum rainfall throughout Bangladesh by location for the selected month.')
st.link_button("Data Source",  "https://www.kaggle.com/datasets/redikod/historical-rainfall-data-in-bangladesh")
st.text("")

# Map the month names in the DataFrame
df['Month'] = df['Month'].map(month_mapping)
df['Year'] = df['Year'].map('{:}'.format)

# Select the month for the bar chart
selected_month = st.selectbox('Select Month:', df['Month'].unique(), index=list(df['Month'].unique()).index(previous_month))
st.text("")

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
        alt.value('#b10f2e'),  # Color for the highest rainfall station
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

# Store the maximum rainfall value before styling
max_rainfall_value = filtered_data['Rainfall'].max()

# Display the dataframe without row numbers and index
filtered_data.reset_index(drop=True, inplace=True)

# Highlight the row with the highest rainfall
max_rainfall_row = filtered_data.iloc[0]
styled_data = filtered_data.style.apply(lambda x: ['background: #b10f2e' if x.name == max_rainfall_row.name else '' for _ in x], axis=1)

# Display the dataframe without row numbers
with st.expander("View Historic Rainfall Data", expanded=False):
    st.subheader(f"Rainfall Data for {selected_month} at {selected_location}")
    st.table(styled_data)

# Filter the latest data for the selected month
if 'Current Month' in latest_df.columns:
    latest_filtered_df = latest_df[latest_df['Current Month'] == selected_month]
else:
    st.write("The 'Month' column is not present in the latest rainfall data.")
    latest_filtered_df = latest_df

# Filter the latest data for the selected location  
latest_filtered_data = latest_filtered_df[latest_filtered_df['Location'] == selected_location]

# Sort the latest filtered data by 'Cumulative' in descending order
latest_filtered_data = latest_filtered_data.sort_values(by='Cumulative', ascending=False)

# Display the latest filtered data
st.text("")
st.subheader(f"🌧️ Latest Rainfall")
st.link_button("Data Source",  "http://www.ffwc.gov.bd/ffwc_charts/rainfall.php")
st.text("")
st.table(latest_filtered_data)

# Compare the latest rainfall data with the historic data
st.text("")
st.subheader("Comparison")

# Find the maximum rainfall in the historic data
historic_max_rainfall = max_rainfall_value

# Find the maximum rainfall in the latest data
latest_max_rainfall = latest_filtered_data['Cumulative'].max()

# Ensure the values are numeric
if pd.isna(latest_max_rainfall) or pd.isna(historic_max_rainfall):
    st.write("Could not compute rainfall comparison due to missing data.")
else:
    # Calculate the difference
    rainfall_diff = latest_max_rainfall - historic_max_rainfall

    if rainfall_diff > 0:
        st.write(f"The maximum rainfall in the latest data ({latest_max_rainfall:.2f}) is {rainfall_diff:.2f} higher than the historic data.")
    elif rainfall_diff < 0:
        st.write(f"The maximum rainfall in the latest data ({latest_max_rainfall:.2f}) is {-rainfall_diff:.2f} lower than the historic data.")
    else:
        st.write("The maximum rainfall in the latest data is the same as the historic data.")

st.divider()
st.text("")
st.subheader("🌊 Latest water levels (WL)")
st.text("📅 " +datetime.datetime.now().strftime("%d %b, %Y"))
st.link_button("Data Source",  "http://www.ffwc.gov.bd/ffwc_charts/waterlevel.php")
st.markdown("Filter the data by 'Show Highlighted Rows' or 'Show All Rows'. Highlighted rows are those with WL Observed values that are at least a specified percentage of the Danger Level.")
st.text("")

# Calculate the highlight condition
def highlight_cells(row):
    return ['background-color: #b10f2e' if (row['WL Observed'] >= (highlight_threshold / 100) * row['Danger Level']) else '' for _ in row]

# Create a filter option with default set to "Show Highlighted Rows"
filter_option = st.selectbox("Select Filter Option:", ["Show All Rows", "Show Highlighted Rows"], index=1)
st.text("")

# Slider for setting the percentage threshold for highlighting
highlight_threshold = st.slider("Set Highlight Threshold (% of Danger Level)", min_value=0, max_value=100, value=90)

# Filter DataFrame based on the selected option
if filter_option == "Show Highlighted Rows":
    # Create a mask for highlighted rows
    highlighted_mask = water_levels_df['WL Observed'] >= (highlight_threshold / 100) * water_levels_df['Danger Level']
    filtered_water_levels_df = water_levels_df[highlighted_mask]
else:
    filtered_water_levels_df = water_levels_df

# Apply the highlight function
styled_water_levels = filtered_water_levels_df.style.apply(highlight_cells, axis=1)

# Display the styled DataFrame in Streamlit
st.text("")
st.table(styled_water_levels)

st.divider()
tanziro = "https://tanziro.com"
repo = "https://github.com/tanzir71/floodcast"
st.subheader("🔔 Early warning system")
st.write("This is a small effort to create an early warning system, so we can plan ahead. You can subscribe to my email list and I will send out an email as soon as the system generates a notification in my local machine.")
st.link_button("Subscribe to Alerts",  "https://mailchi.mp/bf5cff9e7878/floodcast-bangladesh-rainfall-monitoring", type="primary")
st.write("Help improve the [Code](%s)" % repo + " — Low-tech effort ❤️ [Tanzir](%s)" % tanziro)