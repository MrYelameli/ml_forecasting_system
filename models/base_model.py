import os
import pickle
import logging
from abc import ABC, abstractmethod
from utils.logger import setup_logging
import glob

class BaseModel(ABC):
    def __init__(self, config):
        """
        Initializes the BaseModel class with a configuration.
        
        Parameters:
        -----------
        config : dict
            Configuration dictionary loaded from the config file.
        """
        self.config = config
        self.logger = setup_logging()

    @abstractmethod
    def load_data(self, country):
        """
        Abstract method to load data for the model.
        Must be implemented by derived classes.
        """
        pass

    @abstractmethod
    def preprocess_data(self):
        """
        Abstract method to preprocess data for the model.
        Must be implemented by derived classes.
        """
        pass

    @abstractmethod
    def fit(self):
        """
        Abstract method to fit the model.
        Must be implemented by derived classes.
        """
        pass

    @abstractmethod
    def forecast(self):
        """
        Abstract method to forecast using the model.
        Must be implemented by derived classes.
        """
        pass

    def save_model(self, filename):
        """
        Saves the model to a file using pickle.
        
        Parameters:
        -----------
        filename : str
            The name of the file to save the model.
        """
        try:
            model_dir = self.config.get('model_dir', 'models/saved_models')
            os.makedirs(model_dir, exist_ok=True)
            file_path = os.path.join(model_dir, filename)
            
            with open(file_path, 'wb') as f:
                pickle.dump(self.model, f)
            
            self.logger.info(f"Model saved at {file_path}")

        except Exception as e:
            self.logger.error(f"Error saving model: {e}")
            raise

    def get_latest_cleaned_file(self, country):
        """
        Returns the latest cleaned file for the specified country.
        
        Parameters:
        -----------
        country : str
            Name of the country (e.g., 'Country 1' or 'Country 2') for the cleaned file.

        Returns:
        --------
        str
            Path to the latest cleaned file.
        """
        try:
            processed_folder = 'data/processed/'
            search_pattern = f"{processed_folder}CleanedSales{country.replace(' ', '')}_*.xlsx"
            list_of_files = glob.glob(search_pattern)

            if not list_of_files:
                raise FileNotFoundError(f"No cleaned data files found for {country}")
            
            latest_file = max(list_of_files, key=os.path.getctime)
            return latest_file

        except Exception as e:
            self.logger.error(f"Error fetching the latest cleaned file: {e}")
            raise

def execution_time_logger(func):
    """
    Decorator to log the execution time of model methods.
    """
    import time
    def wrapper(*args, **kwargs):
        logger = args[0].logger  # Access the logger from the class instance
        start_time = time.time()
        logger.info(f"Starting '{func.__name__}'...")
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Finished '{func.__name__}' in {end_time - start_time:.2f} seconds.")
        return result
    return wrapper
