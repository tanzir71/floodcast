import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# URL of the webpage to scrape
url = 'http://www.ffwc.gov.bd/ffwc_charts/rainfall.php'

# Send a GET request to the webpage
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the rainfall data
# Assuming the data is in the first table on the page
table = soup.find('table')

# Initialize lists to store the data
locations = []
normals = []
cumulatives = []
current_months = []
current_years = []

# Get the current month and year
current_month = datetime.now().strftime('%B')  # Full month name
current_year = datetime.now().year  # Current year

# Iterate through the rows of the table
for row in table.find_all('tr')[1:]:  # Skip the header row
    cols = row.find_all('td')
    if len(cols) >= 3:  # Ensure there are enough columns
        locations.append(cols[0].text.strip())
        normals.append(cols[1].text.strip())
        cumulatives.append(cols[2].text.strip())
        current_months.append(current_month)  # Add current month to the list
        current_years.append(current_year)  # Add current year to the list

# Create a DataFrame from the lists
rainfall_data = pd.DataFrame({
    'Location': locations,
    'Normal': normals,
    'Cumulative': cumulatives,
    'Current Month': current_months,  # New column for current month
    'Current Year': current_years  # New column for current year
})

# Save the DataFrame to a CSV file
rainfall_data.to_csv('latest_rainfall.csv', index=False)