import pandas as pd
from utils.logger import setup_logging
from datetime import datetime

class DataCleaner:
    def __init__(self):
        """
        Initializes the DataCleaner class and sets up logging.
        """
        self.logger = setup_logging()

    def add_missing_dates(self, data):
        """
        Adds missing dates to the DataFrame with NaN values for the missing rows.

        Parameters:
        -----------
        data : pd.DataFrame
            The input data containing a 'Date' column.

        Returns:
        --------
        pd.DataFrame
            Data with missing dates added and NaN values for other columns.
        """
        try:
            # Ensure the 'Date' column is in datetime format
            data['Date'] = pd.to_datetime(data['Date'])

            # Generate the complete date range from the minimum to maximum date
            full_date_range = pd.date_range(start=data['Date'].min(), end=data['Date'].max(), freq='W-MON')

            # Identify missing dates by comparing with the full date range
            missing_dates = full_date_range.difference(data['Date'])

            # Log all missing dates
            if len(missing_dates) > 0:
                self.logger.info(f"Missing dates found: {len(missing_dates)}")
                for date in missing_dates:
                    self.logger.info(f"Missing date: {date}")
            else:
                self.logger.info("No missing dates found.")

            # Reindex the DataFrame to include the full date range
            data = data.set_index('Date').reindex(full_date_range)

            # Reset the index and rename it back to 'Date'
            data = data.reset_index().rename(columns={'index': 'Date'})

            self.logger.info("Missing dates added successfully.")
            return data

        except Exception as e:
            self.logger.error(f"Error adding missing dates: {e}")
            raise

    def add_national_column(self, data, country):
        """
        Adds a 'National' column for countries that do not have it by summing up all region columns.
        This is only done for Country 1.

        Parameters:
        -----------
        data : pd.DataFrame
            The input data containing region columns.

        country : str
            The name of the country. For Country 1, the 'National' column will be added.

        Returns:
        --------
        pd.DataFrame
            Data with the 'National' column added if applicable.
        """
        try:
            if country == "Country 1" and 'National' not in data.columns:
                # Add National column as the sum of all region columns
                data['National'] = data.filter(like='Region').sum(axis=1)
                self.logger.info("'National' column added for Country 1.")
            else:
                self.logger.info(f"'National' column already exists or not needed for {country}.")

            return data

        except Exception as e:
            self.logger.error(f"Error adding 'National' column: {e}")
            raise

    def set_data_types(self, data):
        """
        Ensures correct data types for each column.

        Parameters:
        -----------
        data : pd.DataFrame
            The input data containing 'Date' and region columns.

        Returns:
        --------
        pd.DataFrame
            Data with corrected data types.
        """
        try:
            # Ensure 'Date' is datetime
            data['Date'] = pd.to_datetime(data['Date'])

            # Ensure all region and national columns are floats (assuming sales data might have decimals)
            region_columns = [col for col in data.columns if 'Region' in col or 'National' in col]
            data[region_columns] = data[region_columns].astype(float)

            self.logger.info("Data types set successfully.")
            return data

        except Exception as e:
            self.logger.error(f"Error setting data types: {e}")
            raise

    def backward_fill(self, data):
        """
        Performs backward filling for all columns except the 'Date' column.

        Parameters:
        -----------
        data : pd.DataFrame
            The input data containing 'Date' and region columns.

        Returns:
        --------
        pd.DataFrame
            The data with missing values filled using backward filling for all columns except 'Date'.
        """
        try:
            # Perform backward fill for all columns except 'Date'
            data_filled = data.fillna(method='bfill', axis=0)

            self.logger.info("Performed backward filling for all columns except 'Date'.")
            return data_filled

        except Exception as e:
            self.logger.error(f"Error during backward filling: {e}")
            raise

    def normalize_column_names(self,data):
        """
        Normalizes column names by converting them to lowercase and replacing spaces with underscores.

        Parameters:
        -----------
        data : pd.DataFrame
            The input data with columns to normalize.

        Returns:
        --------
        pd.DataFrame
            The DataFrame with normalized column names.
        """
        data.columns = data.columns.str.lower().str.replace(' ', '_')
        return data
    
    def save_cleaned_data(self, data, country):
        """
        Saves the cleaned data with a timestamp in the filename.

        Parameters:
        -----------
        data : pd.DataFrame
            The cleaned data to save.

        country : str
            The name of the country (used for file naming).
        """
        try:
            # Get the current timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d')

            # Normalize country name for file naming
            normalized_country_name = country.replace(" ", "")

            # Define the path with the timestamped filename
            cleaned_data_path = f"data/processed/CleanedSales{normalized_country_name}_{timestamp}.xlsx"

            # Save the cleaned data
            data.to_excel(cleaned_data_path, index=False)
            self.logger.info(f"Cleaned data saved at {cleaned_data_path}")

        except Exception as e:
            self.logger.error(f"Error saving cleaned data for {country}: {e}")
            raise



# Example Usage
if __name__ == "__main__":
    # Assuming you have loaded data
    data = pd.read_excel('/home/mry/ml_forecasting_system/data/raw/SalesCountry1.xlsx')  # Example raw data

    cleaner = DataCleaner()

    # Step 1: Add missing dates
    data_with_missing_dates = cleaner.add_missing_dates(data)

    # Step 2: Add National column (for Country 1 only)
    data_with_national = cleaner.add_national_column(data_with_missing_dates, country="Country 1")

    # Step 3: Ensure correct data types
    data_with_correct_types = cleaner.set_data_types(data_with_national)

    # Step 4: Perform backward fill
    cleaned_data = cleaner.backward_fill(data_with_correct_types)

    # step 5: Normalize column names
    cleaned_data = cleaner.normalize_column_names(cleaned_data)

    # Save the cleaned data for inspection
    cleaner.save_cleaned_data(cleaned_data, country="Country 1")
    print("Cleaned data saved.")
