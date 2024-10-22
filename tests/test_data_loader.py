# tests/test_data_loader.py

from src.config_loader import ConfigLoader
from src.data_loader import DataLoader


def test_data_loader():
    # Load the configuration
    config_loader = ConfigLoader(config_path='configs/config.yaml')
    config = config_loader.load_config()

    # Initialize the DataLoader
    data_loader = DataLoader(config)

    # Load the data for both countries
    country_data = data_loader.load_data()

    # Access the loaded data for Country 1 and Country 2
    country_1_data = country_data.get('Country 1')
    country_2_data = country_data.get('Country 2')

    # Basic assertions or checks to verify the data is loaded
    if country_1_data is not None:
        print(f"Country 1 data loaded successfully. Shape: {country_1_data.shape}")
    else:
        print("Country 1 data loading failed.")

    if country_2_data is not None:
        print(f"Country 2 data loaded successfully. Shape: {country_2_data.shape}")
    else:
        print("Country 2 data loading failed.")

# Run the test
if __name__ == "__main__":
    test_data_loader()
