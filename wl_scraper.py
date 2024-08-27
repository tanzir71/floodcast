import requests
from bs4 import BeautifulSoup
import csv
import os

# URL of the webpage
url = 'http://www.ffwc.gov.bd/ffwc_charts/waterlevel.php'

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code != 200:
    print(f"Failed to retrieve data: {response.status_code}")
    exit()

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the data
table = soup.find('table')

# Check if the table was found
if table is None:
    print("No table found on the webpage.")
    exit()

# Read existing data from the CSV file if it exists
existing_data = {}
if os.path.isfile('water_levels.csv'):
    with open('water_levels.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            location = row['Location']
            existing_data[location] = row  # Use location as the key

# Prepare to write to CSV
with open('water_levels.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Location', 'Danger Level', 'WL Observed']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through the rows of the table
    for row in table.find_all('tr')[1:]:  # Skip the header row
        columns = row.find_all('td')
        if len(columns) >= 4:  # Ensure there are enough columns
            location = columns[1].text.strip()
            danger_level = columns[2].text.strip()
            wl_observed = columns[4].text.strip()  # Ensure this is the correct column
            
            # Print scraped data for debugging
            print(f"Scraped Data - Location: {location}, Danger Level: {danger_level}, WL Observed: {wl_observed}")

            if location in existing_data:
                # Update the existing row with the new WL Observed data
                existing_data[location]['WL Observed'] = wl_observed
            else:
                # Add a new row with the new data
                existing_data[location] = {
                    'Location': location,
                    'Danger Level': danger_level,
                    'WL Observed': wl_observed
                }

    # Write the updated data to the CSV file
    writer.writerows(existing_data.values())

print('New WL Observed data has been added to water_levels.csv')