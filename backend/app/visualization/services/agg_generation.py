import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import missingno as msno
from sklearn.impute import SimpleImputer
from datetime import datetime

def replace_outliers_with_mode(data):
        # Calculate the mode for each column
        mode_values = data.mode().iloc[0]

        # Iterate over each column
        for column in data.columns:
            # Calculate Tukey fences
            q1 = data[column].quantile(0.25)
            q3 = data[column].quantile(0.75)
            iqr = q3 - q1
            fence_low = q1 - 1.5 * iqr
            fence_high = q3 + 1.5 * iqr

            # Replace outliers with mode value
            outliers = (data[column] < fence_low) | (data[column] > fence_high)
            data.loc[outliers, column] = mode_values[column]

        return data

 #find patterns in the missing data to seee if there is any correlation among the columns
def treat_missingness(df_replaced):
    ##working with missig values
    #checking for missing values
    # msno.matrix(df_replaced)
    # msno.heatmap(df_replaced, fontsize=5)
    # plt.show()
    #used mode because the missing values are MNAR, heatmap showed a corelation between the columns

    df_nullity = df_replaced.isnull()
    mode_imputer = SimpleImputer(strategy='most_frequent')
    df_replaced.iloc[:, :] = mode_imputer.fit_transform(df_replaced)
    print(df_replaced.isna().sum())
    return df_replaced

#calculate the aggregated daily
def aggregated(df_missingness):
     # Calculate the aggregated daily and monthly generation
    df_missingness.reset_index(inplace=True)
    df_missingness['date_id'] = pd.to_datetime(df_missingness['date_id'], format='%Y-%m-%dT%H:%M:%S')
    df_missingness.set_index('date_id', inplace=True)
    # print(df_replaced.info())
    #picked the numeric columns because i kept getting an error with .mean method from germany col
    numeric_columns = df_missingness.select_dtypes(include=[np.number]).columns
    df_daily = df_missingness[numeric_columns].resample('D').mean()
    df_monthly = df_daily.resample('M').mean()
    # aggregate = {'daily': df_daily, 'monthly': df_monthly}
    return df_daily


def process_data(df):

    # Filter the DataFrame for Germany and set index
    df_germany = df[df["region"] == "Germany"]
    df_germany.set_index("date_id", inplace=True)

    # Pivot the data
    value_by_date_region_vs_generation = df_germany.pivot_table(values="value", index=["date_id", "region"], columns="generation")

    # Replace outliers with mode values
    #considering its power generation its likely the power plant operates within some range and mode is
    #affected by outliers as mean and median

    df_replaced = replace_outliers_with_mode(value_by_date_region_vs_generation)
    df_missingness = treat_missingness(df_replaced)
    
    df_daily = aggregated(df_missingness)
    
    
    return df_daily
    


