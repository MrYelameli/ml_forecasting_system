# Sales Forecasting System

## Project Overview

This project is a **machine learning pipeline** designed to forecast **national-level and region-wise sales** for a product using **time-series data**. The system is built to forecast sales for up to 12 weeks using **Prophet** for national-level forecasting and **XGBoost** for region-wise forecasting. The project is structured to dynamically handle data for different countries and can be extended to future data sources.

---

## Key Features

- **Top-Down Forecasting Approach**:
  - I have adopted a **top-to-bottom hierarchical forecasting approach**. In this approach, we first forecast the **aggregated national-level sales** (including all regions) using **Facebook Prophet**.
  - These forecasted **national-level sales** are then used as a feature for the **subsequent region-based sales forecast** using **XGBoost**.
  - By forecasting at the aggregate level first and then using this information in regional models, we ensure that the overall trends at the national level influence the regional forecasts, capturing broader market trends effectively.

- **National-Level Forecasting**:
  - Uses **Facebook Prophet** to forecast national-level sales.
  - Forecast periods and Prophet parameters are configurable through the `config.yaml` file.
  - Generates a unique forecast file for each country.

- **Region-Wise Forecasting**:
  - Uses **XGBoost** to forecast region-wise sales, leveraging the **national-level forecast** as a feature.
  - Supports the creation of **lagged features** for regional sales, with the number of lag features being parameterized in the config.
  - Generates region-wise forecast files for each country.

- **Data Cleaning Pipeline**:
  - Handles missing dates and fills them with backward filling.
  - Adds a "National" sales column for countries that don't have one by summing up regional sales.
  - Performs data type normalization and column name standardization (lowercase, underscores).
  - Saves cleaned data with timestamps to avoid overwriting.

- **Logging and Monitoring**:
  - Integrated logging tracks the progress of each step in the pipeline, with error handling for any issues that arise.

---

## Folder Structure

```bash
.
├── LICENSE
├── README.md
├── configs
│   └── config.yaml                # Configuration file for parameters and data path
├── data
│   ├── external
│   ├── processed
│   └── raw
│       ├── SalesCountry1.xlsx      # Raw sales data for Country 1
│       └── SalesCountry2.xlsx      # Raw sales data for Country 2
├── environment.yml                 # Environment setup for Conda
├── logs                            # Logs folder for pipeline execution
├── models
│   ├── aggregate_model.py          # Prophet national forecasting model
│   └── xgboost_model.py            # XGBoost region-wise forecasting model
├── notebooks
│   ├── eda_notebooks
│   └── modelling
├── setup.py                        # Project setup
├── src
│   ├── config_loader.py            # Utility to load the config file
│   ├── data_cleaner.py             # Data cleaning and preprocessing
│   └── data_loader.py              # Data loading module
├── tests                           # Unit test folder
└── utils
    ├── __init__.py
    └── logger.py                   # Logging utility
```

## Steps to Run the Project

### 1. Setup the Environment
To set up the environment, use the **`environment.yml`** file with Conda:

```bash
conda env create -f environment.yml
conda activate ml_forecasting_project
```

### 2. Install the Package
```bash
pip install .
```

### 3. Run the Pipeline
```bash
python main.py
```

## Project Flow
1. **Data Cleaning**: The raw sales data is cleaned, missing dates are handled, and region-wise/national sales columns are processed.
2. **National-Level Forecasting**: Prophet forecasts future national sales and saves them in a unique file.
3. **Region-Wise Forecasting**: XGBoost forecasts region-wise sales using the national forecast as a feature and creates lagged features for better predictions.

## Logging
The project uses a logging system to track the progress of each stage of the pipeline, from data cleaning to model training and forecasting. All logs are saved in the logs/ folder.

## Contributing
1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit.
4. Push to the branch.
5. Open a pull request.
