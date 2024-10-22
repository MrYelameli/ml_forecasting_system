# models/base_model.py

import os
import joblib
import pandas as pd
from abc import ABC, abstractmethod
from utils.logger import setup_logging

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

class BaseModel(ABC):
    def __init__(self, config):
        """
        Base class for all models.

        Parameters:
        -----------
        config : dict
            Configuration dictionary loaded from the config file.
        """
        self.config = config
        self.logger = setup_logging()
        self.model = None

    @abstractmethod
    def load_data(self):
        """
        Abstract method to load data. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def preprocess_data(self):
        """
        Abstract method to preprocess data. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def fit(self):
        """
        Abstract method to fit the model. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def forecast(self):
        """
        Abstract method to make forecasts. Must be implemented by subclasses.
        """
        pass

    def save_model(self, model_name):
        """
        Saves the trained model to disk.

        Parameters:
        -----------
        model_name : str
            Name of the model file to save.
        """
        try:
            model_dir = self.config.get('model_dir', 'models')
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, model_name)
            joblib.dump(self.model, model_path)
            self.logger.info(f"Model saved at {model_path}")
        except Exception as e:
            self.logger.error(f"Error saving model: {e}")
            raise

    def load_model(self, model_name):
        """
        Loads a trained model from disk.

        Parameters:
        -----------
        model_name : str
            Name of the model file to load.
        """
        try:
            model_dir = self.config.get('model_dir', 'models')
            model_path = os.path.join(model_dir, model_name)
            self.model = joblib.load(model_path)
            self.logger.info(f"Model loaded from {model_path}")
        except Exception as e:
            self.logger.error(f"Error loading model: {e}")
            raise

    def log_performance(self, performance_metrics):
        """
        Logs the performance metrics of the model.

        Parameters:
        -----------
        performance_metrics : dict
            Dictionary containing performance metrics.
        """
        for metric, value in performance_metrics.items():
            self.logger.info(f"{metric}: {value}")

