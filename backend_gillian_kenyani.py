import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import missingno as msno
from sklearn.impute import SimpleImputer
from datetime import datetime



#make an API call and store the response

base_url = "https://api.agora-energy.org/publicdata/api"
api_key= "agora_api_DCB21HjFwwK%wyhHyD1%HU4w22F6zw.9jh&zkOkj1H"
dataset = "task_generation_h"
date_from = "2022-10-01"
date_to = "2022-12-31"

headers = {
    "API-Key": api_key
}

params = {
    "dataset": dataset,
    "from": date_from,
    "to": date_to
}


try:
    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    # print(data)
    #convert into a dataframe by accesing the data key in the dict
    # , columns = [data["columns"]]
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    df=pd.DataFrame(data["data"])
    df.columns = data["columns"]
    # print(df.head())
    # print(df.info())

    #filtering with Germany

    df_germany = df[df["region"] == "Germany"]

    
    # print(df_germany.head())
    # print(df.dtypes)
  
    
    df_germany.set_index("date_id", inplace=True)
    print(df_germany.head())

    #pivoting the data
    value_by_date_region_vs_generation = df_germany.pivot_table(values="value", index=["date_id","region"], columns="generation")

    pivot_summary = value_by_date_region_vs_generation.describe()
    summary_stat = df_germany.describe()

    # print(value_by_date_region_vs_generation.head())

    #######plotting to visualize before treating outliers
    plt.figure(figsize=(14, 8))
    plt.boxplot(value_by_date_region_vs_generation.values, labels=value_by_date_region_vs_generation.columns)
    plt.title('Box Plot of Generation Data pre outlier treatment')
    plt.xlabel('Generation Type')
    plt.ylabel('Generation Value')
    plt.xticks(fontsize=3)
    #plt.show()

    ####### treating the outliers-replacing with the mode, mean and median are affected by the extreme values
    #since its generation, its likely that power output frequents a certain MW since demand is relatively around same value
    # print(pivot_summary)

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
    
    df_replaced = replace_outliers_with_mode(value_by_date_region_vs_generation)
    print("outlier treatment")
    print(df_replaced.head())
    # print(df_replaced.describe())
    ####plot the figure after compare the box plots

    plt.figure(figsize=(14, 8))
    plt.boxplot(df_replaced.values, labels=df_replaced.columns)
    plt.title('Box Plot of Generation Data post outlier treatment')
    plt.xlabel('Generation Type')
    plt.ylabel('Generation Value')
    plt.xticks(fontsize=3)
    #plt.show()
    

    #check for missing values


    print(value_by_date_region_vs_generation.Solar[value_by_date_region_vs_generation.Solar > 0])
    #convert index column into a regular column
    # df_replaced_reset = df_replaced.reset_index()
    # value_by_date_region_vs_generation=value_by_date_region_vs_generation.reset_index()
    
    # #visualizing sola and pup storage ,before replacing with mode,  since it has IQR of 0
    # plt.figure(figsize=(12, 8))  # Increase the figure size (width: 12 inches, height: 8 inches)
    # plt.scatter(value_by_date_region_vs_generation.index, value_by_date_region_vs_generation['Solar'], label='Solar')
    # plt.scatter(value_by_date_region_vs_generation.index, value_by_date_region_vs_generation['Pumped storage generation'], label='Pumped storage generation')
    # plt.title('Scatter Plot of Generation Data before replacing outliers')
    # plt.xlabel('Date')
    # plt.ylabel('Generation Value')
    # plt.legend()
    # plt.xticks(rotation=45)
    # plt.show()

    #  #visualizing sola and pup storage ,After replacing with mode
    # plt.figure(figsize=(12, 8))  # Increase the figure size (width: 12 inches, height: 8 inches)
    # plt.scatter(df_replaced_reset.index, df_replaced_reset['Solar'], label='Solar')
    # plt.scatter(df_replaced_reset.index, df_replaced_reset['Pumped storage generation'], label='Pumped storage generation')
    # plt.title('Scatter Plot of Generation Data After replacing outliers')
    # plt.xlabel('Date')
    # plt.ylabel('Generation Value')
    # plt.legend()
    # plt.xticks(rotation=45)
    # plt.show()

    #the plots looks the same, i think because our mean is pulled to zero traetment wasnt effective?
    print(df_replaced.isna().any())
    print(df_replaced.head())
    
    #find the missing data and why its missing 
    #visualize missing values

    df_nullity = df_replaced.isnull()
    # print(df_replaced.describe())
  
    #find patterns in the missing data to seee if there is any correlation among the columns

    msno.matrix(df_replaced)
    msno.heatmap(df_replaced, fontsize=5)
    #there is a corelation 0f 0.9 between nuclear and non-renewable waste mising values
    #makes sense that they are dependecies since nuclear is considered non renewable
    #corelation between the waste and other renewable, since some renewable produce non-renewable waste like biodiesel?
    
    #plt.show()
    
    #how to treat the missing values
    #used mode because the missing values are MNAR,
    #create a copy of the dataset to compare later
    df_replaced_mode = df_replaced.copy(deep=True)
    mode_imputer = SimpleImputer(strategy='most_frequent')
    df_replaced_mode.iloc[:, :] = mode_imputer.fit_transform(df_replaced_mode)
    
    print("isna? after imputing missing values")
    print(df_replaced_mode.isna().sum())
    
    #visualize box plot again
    plt.figure(figsize=(14, 8))
    plt.boxplot(df_replaced_mode.values, labels=df_replaced_mode.columns)
    plt.title('Box Plot of Generation Data post missing values treatment')
    plt.xlabel('Generation Type')
    plt.ylabel('Generation Value')
    plt.xticks(fontsize=3)
    #plt.show()

    
    # df_replaced_mode_reset = df_replaced_mode.reset_index()
    # plt.figure(figsize=(12, 8))  # Increase the figure size (width: 12 inches, height: 8 inches)
    # plt.scatter(df_replaced_mode_reset.index, df_replaced_mode_reset['Solar'], label='Solar')
    # plt.scatter(df_replaced_mode_reset.index, df_replaced_mode_reset['Pumped storage generation'], label='Pumped storage generation')
    # plt.title('Scatter Plot of Generation Data After replacing outliers')
    # plt.xlabel('Date')
    # plt.ylabel('Generation Value')
    # plt.legend()
    # plt.xticks(rotation=45)
    # plt.show()

   
    # print(df_replaced_mode.sort_values("Solar").head(20))
    # print("descending")
    # print(df_replaced_mode.sort_values("Solar", ascending=False).head(20))
    # mean = df_replaced['Solar'].mean()
    # print(df_replaced_mode.describe())

    #calculate the aggregated daily and monthly gen
    # print(df_replaced_mode.head())
    
    ###creating time series
   
   
    # print(df_replaced_mode.head())
    # print(df_replaced_mode.dtypes)
    df_replaced_mode.reset_index(inplace=True)
    df_replaced_mode['date_id'] = pd.to_datetime(df_replaced_mode['date_id'], format='%Y-%m-%d %H:%M:%S')
    df_replaced_mode.set_index('date_id', inplace=True)
    # print("df_replaced_mode")
    # print(df_replaced_mode.head())
    
    # Calculate the aggregated daily generation for each type
    df_daily = df_replaced_mode.resample('D').asfreq()
    # print("daily generation")
    # print(df_daily.head())
   
    # print(df_replaced_mode.info())

    # Calculate the aggregated monthly generation for each type
   
    df_monthly = df_daily.resample('M').mean()
    # print("miontly generation")
    # print(df_monthly.head())
    # print(df_replaced_mode.head())

    
    #print("daily########")
    #print(df_daily.head())
    df_daily.reset_index(inplace=True)
    print("reset index")
    #print(df_daily.head())
    df_daily_json = df_daily.to_json(orient='index')
    #print(df_daily_json)
    print(df_daily.columns)
    
    #print("json")
    #print(df_daily_json)

    file_path = './data'

    # Save the DataFrame to the CSV file option
    # df_daily_json = df_daily.to_json(orient='columns')
    # df_daily.to_csv(file_path, index=True)

    
    renewable_sources = ['Biomass', 'Dam Hydro', 'Geothermal', 'Other renewables',
                     'Pumped storage generation', 'Run-of-River Hydro',
                     'Solar', 'Wind offshore', 'Wind onshore']

    non_renewable_sources = ['Hard Coal', 'Lignite', 'Natural Gas', 'Non-renewable waste',
                         'Nuclear', 'Oil', 'Other fossil fuel']

    renewable_generation = df_replaced_mode[df_replaced_mode.columns[df_replaced_mode.columns.isin(renewable_sources)]]
    # print("renewable")
    # print(renewable_generation.head())
    non_renewable_generation = df_replaced_mode[df_replaced_mode.columns[df_replaced_mode.columns.isin(non_renewable_sources)]]

    #hourly generation renewable

    #aggregated daily renewable
    #aggregated monthly renewable
    # print(renewable_generation.head())
    # print(df_replaced_mode.columns)
    # Hourly electricity generation
    hourly_table = pd.pivot_table(df_replaced_mode, index=df_replaced_mode.index.hour,
                                  values=renewable_sources+non_renewable_sources,
                                  aggfunc='sum', margins=True)
    # print("renewable hourly")
    # print(hourly_table)

    # Daily electricity generation
    daily_table = pd.pivot_table(df_replaced_mode, index=df_replaced_mode.index.date,
                                 values=renewable_sources+non_renewable_sources,
                                 aggfunc='sum', margins=True, margins_name='Total')

    # Monthly electricity generation
    monthly_table = pd.pivot_table(df_replaced_mode, index=df_replaced_mode.index.to_period('M'),
                                   values=renewable_sources+non_renewable_sources,
                                   aggfunc='sum', margins=True, margins_name='Total')
    

    # # # Calculate the percentage of total generation
    #calculating the aggregated renewable 
    # df_daily_renewable_generation = renewable_generation.resample('D').mean()
    # df_daily_renewable_generation_pivot =pd.pivot_table(df_daily_renewable_generation, index=df_daily_renewable_generation.index.hour,
    #                               values=renewable_sources,
    #                               aggfunc='sum', margins=True)
    # print("col  df_daily_renewable_generation_pivot")
    # print( df_daily_renewable_generation_pivot.columns)
    # print( df_daily_renewable_generation_pivot.head())
    

    # #aggregated renewable monthly
    # df_monthly_renewable_generation =  df_daily_renewable_generation.resample('M').mean()

    # #calculating the aggregated non-renewable 
    # df_daily_non_renewable_generation = non_renewable_generation.resample('D').mean()

    # #aggregated non renewable
    # df_monthly_non_renewable_generation =  df_daily_non_renewable_generation.resample('M').mean()





    # hourly_table_percent = (hourly_table / hourly_table['Total']) * 100
    # daily_table_percent = (daily_table / daily_table['Total']) * 100
    # monthly_table_percent = (monthly_table / monthly_table['Total']) * 100

    # print(hourly_table_percent)
    # print(daily_table_percent)
    # print(monthly_table_percent)
    # print( monthly_table.head())


 
 

 
#handling errors related to API call
except requests.RequestException as e:
    print("Error:", e)
#handling errors related to parsing the response
except ValueError as e:
    print("Error: Invalid response format -", e)



