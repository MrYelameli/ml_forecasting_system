import yaml
import os
from utils.logger import setup_logging

class ConfigLoader:
    """
    A class to load and parse the configuration YAML file.
    
    Attributes:
    -----------
    config_path : str
        The path to the YAML configuration file.
    config : dict
        A dictionary to store the loaded configuration.
    
    Methods:
    --------
    load_config():
        Loads the YAML configuration file and returns it as a dictionary.
    """
    
    def __init__(self, config_path='configs/config.yaml'):
        """
        Initializes the ConfigLoader with the path to the configuration file.

        Parameters:
        -----------
        config_path : str
            Path to the YAML configuration file.
        """
        self.config_path = config_path
        self.config = None
        self.logger = setup_logging()

    def load_config(self):
        """
        Loads the YAML configuration file and stores the content in the config attribute.

        Returns:
        --------
        dict
            Loaded configuration as a dictionary.
        """
        try:
            self.logger.info(f"Loading configuration from: {self.config_path}")
            # Check if the configuration file exists
            if not os.path.exists(self.config_path):
                raise FileNotFoundError(f"Configuration file not found at: {self.config_path}")

            # Load the YAML file
            with open(self.config_path, 'r') as file:
                self.config = yaml.safe_load(file)
                self.logger.info("Configuration loaded successfully.")
                return self.config

        except yaml.YAMLError as exc:
            self.logger.error(f"Error parsing the YAML configuration file: {exc}")
            raise

        except Exception as e:
            self.logger.error(f"An error occurred while loading the configuration: {e}")
            raise

# config_loader = ConfigLoader(config_path='configs/config.yaml')
# config = config_loader.load_config()

# # Accessing data paths
# country_1_data_path = config['data_paths']['country_1']
# print(f'country_1_data_path: {country_1_data_path}')
# country_2_data_path = config['data_paths']['country_2']
# print(f'country_2_data_path: {country_2_data_path}')

# # Accessing model parameters for country 1
# prophet_params_country_1 = config['model_params']['country_1']['prophet']
# print(f'prophet_params_country_1: {prophet_params_country_1}')
# xgboost_params_country_1 = config['model_params']['country_1']['xgboost']
# print(f'xgboost_params_country_1: {xgboost_params_country_1}')

# # Accessing model parameters for country 2
# prophet_params_country_2 = config['model_params']['country_2']['prophet']
# print(f'prophet_params_country_2: {prophet_params_country_2}')
# xgboost_params_country_2 = config['model_params']['country_2']['xgboost']
# print(f'xgboost_params_country_2: {xgboost_params_country_2}')
