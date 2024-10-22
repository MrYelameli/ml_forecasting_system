from src.config_loader import ConfigLoader
from models.aggregate_model import ProphetModel
from src.data_cleaner import DataCleaner  # Adjust import path as needed


if __name__ == "__main__":
    # Load configuration
    config_loader = ConfigLoader(config_path='configs/config.yaml')
    config = config_loader.load_config()

    # Initialize and test Prophet model
    prophet_model = ProphetModel(config)

    country_to_process = 'country_1'

    # Step 1: Load the data
    prophet_model.load_data(country=country_to_process)

    # Step 2: Preprocess the data
    prophet_model.preprocess_data()

    # Step 3: Fit the model
    prophet_model.fit()

    # Step 4: Forecast future data
    prophet_model.forecast()

    print("Prophet model test completed.")
