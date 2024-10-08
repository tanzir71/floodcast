# Flood Monitor — Rainfall Data for Bangladesh

## Description
The project aims to provide flood forecasting and early warning systems for communities prone to flooding.

## Structure
The gaol is to run the service with minimal overhead. Individual scrapers gather data based on the data refresh frequency of the source. The system utilizes GitHub Actions to run these scrapers, which updates the CSV and the Streamlit deployment automatically updates every time there's a new update to the repository.

## Contributing
We welcome contributions to the Floodcast project. If you would like to contribute, please follow these guidelines:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure they pass all tests.
4. Submit a pull request with a detailed description of your changes.
