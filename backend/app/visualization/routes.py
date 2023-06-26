from flask import Flask, json, request, Blueprint, render_template
import requests
import pandas as pd
from .services.agg_generation import process_data
from io import StringIO




blueprint = Blueprint('api', __name__)

#fetch the data from the api

def fetch_data_from_api(api_key, dataset, date_from, date_to):
    base_url = "https://api.agora-energy.org/publicdata/api"
    
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

        df = pd.DataFrame(data["data"])
        df.columns = data["columns"]

        # print("Column names:", df.columns) 
        # df.set_index("date_id", inplace=True)

        return df
    
    except requests.RequestException as e:
        print("Error:", e)
        return None
    except ValueError as e:
        print("Error: Invalid response format -", e)
        return None

    #define api params
base_url = "https://api.agora-energy.org/publicdata/api"
api_key= "agora_api_DCB21HjFwwK%wyhHyD1%HU4w22F6zw.9jh&zkOkj1H"
dataset = "task_generation_h"
date_from = "2022-10-01"
date_to = "2022-12-31"


# Fetch data from API
df = fetch_data_from_api(api_key, dataset, date_from, date_to)
# print(df.info())
# print(df.head())


#   df_daily = process_data(df)
#     # df_monthly_csv = df_monthly.to_csv(index=True)
#     df_daily = df_daily.to_dict(orient='records')



#return the data
@blueprint.route('/')
def index():
    # aggregated_data = process_data(df)

    # # df_daily = aggregated_data['daily']
    # df_monthly = aggregated_data['monthly']

    df_daily= process_data(df)

    # # Convert df_daily to the appropriate format for D3
    # df_daily_data = df_daily.reset_index().to_dict(orient='records')
    
    # # Convert df_monthly to the appropriate format for D3
    # df_monthly_data = df_monthly.reset_index().to_dict(orient='records')
    #    # Convert data to JSON format
    # df_daily_json = json.dumps(df_daily_data)
    # df_monthly_json = json.dumps(df_monthly_data)
    #convert to csv
    # df_daily_csv = df_daily.reset_index().to_csv(index=False)
    # df_monthly_data = df_monthly.reset_index().to_dict(orient='records')

    df_daily_json = df_daily.to_json(orient='columns')
    # df_monthly_json = df_monthly.to_json(orient='columns')


    return render_template('index.html', df_daily=df_daily_json)

