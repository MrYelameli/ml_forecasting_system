from models.base_model import BaseModel, execution_time_logger
from prophet import Prophet
import xgboost as xgb
import pandas as pd
import os
from utils.logger import setup_logging
from datetime import datetime

class XGBoostModel(BaseModel):
    def __init__(self, config):
        """
        Initializes the XGBoost model class.
        
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
        Loads the cleaned regional data and national-level forecast for the given country.
        """
        try:
            # Load cleaned data for the country
            country_config = self.config['countries'][country]
            # cleaned_data_path = f"data/processed/CleanedSales{country_config['name'].replace(' ', '')}.xlsx"
            cleaned_data_path = self.get_latest_cleaned_file(country_config['name'])
            data = pd.read_excel(cleaned_data_path)
            self.logger.info(f"Cleaned data loaded from {cleaned_data_path}")
            
            # Load the national-level forecast as a feature
            national_forecast_path = f"data/forecasts/prophet_forecast_{country}.xlsx"
            national_forecast = pd.read_excel(national_forecast_path)
            
            # Filter historical dates
            historical_dates = data['date']
            national_forecast_filtered = national_forecast[national_forecast['ds'].isin(historical_dates)]
            
            # Merge national forecast with historical data
            data = pd.merge(data, national_forecast_filtered[['ds', 'yhat']], left_on='date', right_on='ds', how='left')
            data.drop(columns=['ds'], inplace=True)
            self.logger.info("National forecast merged with historical data.")
            
            # Generate lagged features
            region_columns = ['region_1', 'region_2', 'region_3']
            num_lags = self.config['countries'][country].get('num_lags', 4)
            data_with_lags = self.create_lagged_features(data, region_columns, 'national', num_lags)

            # Drop the 'date' and region columns for XGBoost features
            X = data_with_lags.drop(columns=['region_1', 'region_2', 'region_3'])
            y = data_with_lags[['region_1', 'region_2', 'region_3']]
            
            return X, y

        except Exception as e:
            self.logger.error(f"Error loading data for {country}: {e}")
            raise

    def create_lagged_features(self, data, region_columns, national_column, num_lags=7):
        """
        Creates lagged features for regional sales and adds the national forecast as a feature.
        
        Parameters:
        -----------
        data : pd.DataFrame
            Data containing regional sales and national forecast.
        region_columns : list
            List of regional sales column names.
        national_column : str
            Column name for national sales forecast.
        num_lags : int
            Number of lagged features to create.
        
        Returns:
        --------
        pd.DataFrame:
            DataFrame with lagged features added.
        """
        for region in region_columns:
            for lag in range(1, num_lags + 1):
                data[f'{region}_lag{lag}'] = data[region].shift(lag)
        
        data['National_forecast'] = data[national_column]
        
        # Drop rows with NaN values resulting from lagging
        data = data.dropna()
        return data

    @execution_time_logger
    def fit(self, X, y, country):
        """
        Train the XGBoost model on the full dataset.
        """
        try:
            region_models = {}
            for region in y.columns:
                model_params = self.config['model_params'][country]['xgboost']
                model = xgb.XGBRegressor(**model_params)
                model.fit(X.drop(columns=['date']), y[region])
                region_models[region] = model
                self.logger.info(f"XGBoost model trained for {region} in {country}.")
            
            self.model = region_models

        except Exception as e:
            self.logger.error(f"Error training XGBoost model for {country}: {e}")
            raise

    @execution_time_logger
    def forecast(self, X_future, country, forecast_periods=12):
        """
        Forecast the next 12 periods using the XGBoost model.
        """
        try:
            # Create a DataFrame to store forecast results
            forecast = pd.DataFrame()

            # Generate future dates
            future_dates = pd.date_range(start=pd.to_datetime(X_future['date'].max()) + pd.DateOffset(weeks=1), 
                                         periods=forecast_periods, freq='W-MON')
            forecast['date'] = future_dates

            # Drop the 'date' column from X_future
            X_future = X_future.drop(columns=['date'])

            # Forecast for each region
            for region, model in self.model.items():
                # Ensure the X_future only has the next 12 data points
                forecast[region] = model.predict(X_future.iloc[-forecast_periods:])

            # Save forecast to a CSV or Excel file
            output_path = f"data/forecasts/region_forecast_{country}.xlsx"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            forecast.to_excel(output_path, index=False)
            self.logger.info(f"Region-wise forecast saved at {output_path}")

        except Exception as e:
            self.logger.error(f"Error forecasting region-wise sales for {country}: {e}")
            raise

    def preprocess_data(self):
        pass