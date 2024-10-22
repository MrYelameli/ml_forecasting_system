from src.config_loader import ConfigLoader
from models.aggregate_model import ProphetModel  
from models.item_model import XGBoostModel  # Import XGBoost model
from src.data_cleaner import DataCleaner
from utils.logger import setup_logging
import pandas as pd

def main():
    # Set up logging
    logger = setup_logging()
    
    try:
        # Step 1: Load configuration
        logger.info("Loading configuration...")
        config_loader = ConfigLoader(config_path='configs/config.yaml')
        config = config_loader.load_config()
        logger.info("Configuration loaded successfully.")

        # Step 2: Data cleaning
        logger.info("Starting data cleaning process...")
        cleaner = DataCleaner()
        for country in config['countries']:
            logger.info(f"Cleaning data for {config['countries'][country]['name']}...")
            raw_data_path = config['countries'][country]['data_path']
            data = pd.read_excel(raw_data_path)  # Load raw data for cleaning
            cleaned_data = cleaner.add_missing_dates(data)
            cleaned_data = cleaner.add_national_column(cleaned_data, country=config['countries'][country]['name'])
            cleaned_data = cleaner.set_data_types(cleaned_data)
            cleaned_data = cleaner.backward_fill(cleaned_data)
            cleaned_data = cleaner.normalize_column_names(cleaned_data)
            cleaner.save_cleaned_data(cleaned_data, country=config['countries'][country]['name'])
            logger.info(f"Data cleaned and saved for {config['countries'][country]['name']}.")

        # Step 3: National-level forecasting with Prophet
        logger.info("Starting national-level forecasting using Prophet...")
        prophet_model = ProphetModel(config)
        
        for country in config['countries']:
            logger.info(f"Processing forecasting for {config['countries'][country]['name']}...")
            prophet_model.load_data(country=country)
            prophet_model.preprocess_data()
            prophet_model.fit()
            prophet_model.forecast(country=country)
            logger.info(f"National-level forecast completed for {config['countries'][country]['name']}.")

            # Step 4: Region-wise forecasting with XGBoost
        logger.info("Starting region-wise forecasting using XGBoost...")
        xgboost_model = XGBoostModel(config)

        for country in config['countries']:
            logger.info(f"Loading cleaned data and national forecast for {config['countries'][country]['name']}...")

            # Load the entire dataset for training and forecasting
            X, y = xgboost_model.load_data(country=country)
            
            # Train XGBoost models for each region
            xgboost_model.fit(X, y, country=country)
            logger.info(f"XGBoost model training completed for {config['countries'][country]['name']}.")

            # Forecast for the next 12 periods
            logger.info(f"Forecasting region-wise sales for {config['countries'][country]['name']}...")
            xgboost_model.forecast(X, country=country)
            logger.info(f"Region-wise forecasting completed for {config['countries'][country]['name']}.")

        logger.info("Pipeline completed successfully.")

    except Exception as e:
        logger.error(f"Error occurred during the pipeline execution: {e}")
        raise

if __name__ == "__main__":
    main()
