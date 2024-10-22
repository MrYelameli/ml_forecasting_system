import pandas as pd
from src.config_loader import ConfigLoader
from utils.logger import setup_logging


class DataLoader:
    def __init__(self, config):
        """
        Initialize DataLoader with the configuration.
        
        Parameters:
        -----------
        config : dict
            Dictionary containing the configuration, including paths for Country 1 and Country 2.
        """
        self.config = config
        self.logger = setup_logging()

    def load_country_data(self, country_name, data_path):
        """
        Load data for a given country.

        Parameters:
        -----------
        country_name : str
            The name of the country being loaded.
        data_path : str
            Path to the Excel file for the country data.

        Returns:
        --------
        pd.DataFrame
            The loaded data for the country.
        """
        try:
            self.logger.info(f"Loading data for {country_name} from {data_path}...")
            data = pd.read_excel(data_path)
            self.logger.info(f"Successfully loaded data for {country_name}.")
            return data
        except Exception as e:
            self.logger.error(f"Error loading data for {country_name}: {e}")
            raise

    def load_data(self):
        """
        Load data for both Country 1 and Country 2 sequentially.

        Returns:
        --------
        dict
            A dictionary containing data for both countries, with country names as keys.
        """
        data_paths = self.config['countries']

        country_data = {}
        for country_key, country_info in data_paths.items():
            country_name = country_info['name']
            data_path = country_info['data_path']

            # Load data for each country and store in the dictionary
            country_data[country_name] = self.load_country_data(country_name, data_path)

        return country_data

# if __name__ == "__main__":
#     # Import the necessary modules
#     from config_loader import ConfigLoader

#     # Initialize the ConfigLoader
#     config_loader = ConfigLoader(config_path='../configs/config.yaml')  # Adjust path as needed
#     config = config_loader.load_config()

#     # Initialize DataLoader with the loaded config
#     data_loader = DataLoader(config)

#     # Test data loading for both countries
#     country_data = data_loader.load_data()

#     # Access data for Country 1 and Country 2
#     country_1_data = country_data.get('Country 1')
#     country_2_data = country_data.get('Country 2')

#     # Print some information about the data for manual testing
#     if country_1_data is not None:
#         print(f"Country 1 Data Loaded: {country_1_data.shape}")
#     else:
#         print("Failed to load Country 1 data")

#     if country_2_data is not None:
#         print(f"Country 2 Data Loaded: {country_2_data.shape}")
#     else:
#         print("Failed to load Country 2 data")
