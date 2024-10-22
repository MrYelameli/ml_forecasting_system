from models.base_model import BaseModel, execution_time_logger
from prophet import Prophet
import xgboost as xgb
import pandas as pd
import os
from utils.logger import setup_logging
from datetime import datetime


class ProphetModel(BaseModel):
    def __init__(self, config):
        """
        Initializes the ProphetModel class.
        
        Parameters:
        -----------
        config : dict
            Configuration dictionary loaded from the config file.
        """
        super().__init__(config)
        self.model = None  # Will be initialized during training

    @execution_time_logger
    def load_data(self, country):
        """
        Loads and prepares the data for the Prophet model.
        """
        try:
            # Load national-level data
            country_config = self.config['countries'][country]
            cleaned_data_path = self.get_latest_cleaned_file(country_config['name'])
            self.data = pd.read_excel(cleaned_data_path)
            self.logger.info(f"Cleaned data loaded from {cleaned_data_path}")

            # Ensure date column is in datetime format
            self.data['date'] = pd.to_datetime(self.data['date'])

        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            raise

    @execution_time_logger
    def preprocess_data(self):
        """
        Prepares the data for the Prophet model by renaming and filtering columns.
        """
        try:
            # Select only necessary columns for Prophet ('ds' for date, 'y' for target)
            self.data = self.data.rename(columns={'date': 'ds', 'national': 'y'})
            self.logger.info("Data preprocessing completed for Prophet.")

        except Exception as e:
            self.logger.error(f"Error preprocessing data: {e}")
            raise

    @execution_time_logger
    def fit(self):
        """
        Fits the Prophet model on the data.
        """
        try:
            self.model = Prophet(**self.config.get('model_params', {}).get('prophet', {}))
            self.model.fit(self.data)
            self.logger.info("Prophet model training complete.")

            # Save the trained Prophet model
            self.save_model('prophet_model.pkl')

        except Exception as e:
            self.logger.error(f"Error fitting Prophet model: {e}")
            raise

    @execution_time_logger
    def forecast(self, country):
        """
        Makes future predictions using the Prophet model.
        """
        try:
            # Forecast for the next configured period
            forecast_periods = self.config['countries'][country].get('forecast_periods', 12)
            future = self.model.make_future_dataframe(periods=forecast_periods, freq='W-MON')
            self.forecast_df = self.model.predict(future)
            self.logger.info(f"Forecasting for {country} complete.")

            # Save forecast to a CSV or Excel file
            output_path = f"data/forecasts/prophet_forecast_{country}.xlsx"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            self.forecast_df.to_excel(output_path, index=False)
            self.logger.info(f"Forecast saved at {output_path}")

        except Exception as e:
            self.logger.error(f"Error during forecasting: {e}")
            raise




