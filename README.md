# Energy Data Analysis in Germany Renewable vs Non-Renewable Sources
Scope: Analysis of electricity generation by fuel type in Germany (October–December 2022).

## Project Overview

This project ingests, cleans, treats, and visualizes electricity generation data for Germany, distinguishing renewable and non-renewable sources. 

 
## Features

* Fetch data from API or load local cache.
* Outlier detection and replacement (hour & month-based median).
* Missing data imputation using linear interpolation.
* Aggregation by fuel type, renewable vs non-renewable.
* Visualization of energy generation trends using stacked area plot and bar charts.


## Environment
Project uses a Python virtual environment (venv) to manage dependencies.
and  environment variables  BASE_URL, API_KEY.

## Data
Input: Hourly electricity generation by fuel type.
Output:
Cleaned hourly data: germany_hourly_by_fuel_cleaned.csv
Daily & monthly aggregates: germany_daily_by_fuel_MWh.csv, germany_monthly_by_fuel_MWh.csv
Renewable vs non-renewable: germany_hourly_renewable_nonrenewable.csv, germany_daily_renewable_nonrenewable.csv, germany_monthly_renewable_nonrenewable.csv
Long format hourly data: germany_hourly_long.csv
Figures: figure_bar_comparison_sources_GWh.png,figure_stacked_area_daily_GWh.png, figure_renewable_vs_nonrenewable_Oct_Dec_GWh.png

## Setup
* Clone the repository
* Create a virtual environment and activate it:
    python -m venv venv
    source venv/bin/activate 
* install dependencies
    pip install -r requirements.txt
* create .env and add the variables:
    BASE_URL=<base_url>
    API_KEY=<api_key>
* Run the Jupyter Notebook
