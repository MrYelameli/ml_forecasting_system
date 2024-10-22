import os
import glob

def get_latest_cleaned_file(country):
    """
    Returns the latest cleaned file for the specified country from the processed data folder.

    Parameters:
    -----------
    country : str
        The name of the country (e.g., 'Country 1').

    Returns:
    --------
    str
        Path to the latest cleaned data file.
    """
    processed_folder = 'data/processed/'
    search_pattern = f"{processed_folder}CleanedSales{country}_*.xlsx"
    list_of_files = glob.glob(search_pattern)
    
    if not list_of_files:
        raise FileNotFoundError(f"No cleaned data files found for {country}")
    
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def normalize_country_name(country_name):
    """
    Converts a country name to a file-friendly format (e.g., removes spaces).
    
    Parameters:
    -----------
    country_name : str
        The original country name from the configuration.
    
    Returns:
    --------
    str
        A normalized country name suitable for file paths.
    """
    return country_name.replace(" ", "")  # Remove spaces or modify as needed

