# _______________ LOAD_DATA.PY _______________

# CONTAINS ALL FUNCTION TO GET DATA BETWEEN TWO DATE 
# THIS FILE USE THE CSV HISTORY FOR BETTER PERFORMANCE
# AND GET NEW DATA IN REAL-TIME

import requests
import urllib.parse
import pandas as pd
import numpy as np
from datetime import date, timedelta




def getWeatherDataFromServer(begin_date:date,end_date:date) -> np.array:
    """Get all the data between dates for a MAXIMUM of (365 days) by requeting the server

    Args:
        begin_date (date): _description_
        end_date (date): _description_

    Returns:
        np.array: _description_
    """
    
    DAY_DURATION = 24
    YEAR_DURATION = 365
    ALL_RAIN_DATA = []

    if ((end_date-begin_date).days) > YEAR_DURATION:
        raise ValueError("Attention l'écart entre les deux dates dépassent 1 an")

    base_url = "https://www.infoclimat.fr/opendata/"
    params = {
        "version": "2",
        "method": "get",
        "format": "json",
        "stations[]": "07690",
        "start": begin_date.strftime("%Y-%m-%d"),
        "end": end_date.strftime("%Y-%m-%d"), # AAAA-MM-DD
        "token": "eZucxR2pA3oDfiWFlItshDc2Yzj9OIYSGevDhKtx9KZmkBjfedXQ",
    }

    query_string = "&".join([f"{key}={urllib.parse.quote(str(value))}" for key, value in params.items()])
    API_URL = f"{base_url}?{query_string}"

    try:
        response = requests.get(API_URL)

        if response.status_code == 200:
            data = response.json()
     
            cum_rain_in_day = 0
            idx_24_hours = 0

            for data_in_hour in data["hourly"]["07690"]:
                pluie_1h = data_in_hour.get("pluie_1h", 0) or 0
                cum_rain_in_day += float(pluie_1h)
                idx_24_hours += 1

                if idx_24_hours % DAY_DURATION == 0:
                    ALL_RAIN_DATA.append(round(cum_rain_in_day, 1))
                    cum_rain_in_day = 0
                    idx_24_hours = 0

            print(f"Success: Data retrieved for year period {begin_date} to {end_date}")
        else:
            print(f"Error: {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error during request: {e}")

    return ALL_RAIN_DATA



def getHistoricalRainFallBetweenDates(begin_date: date, end_date: date):

    YEAR_DURATION = 365  
    no_day_between = (end_date - begin_date).days
    
    if no_day_between <= 0:
        raise ValueError("La date de début doit être antérieure à la date de fin.")
    
    new_date_retrieve = begin_date
    ALL_DATA_RAIN_PERIOD = np.array([])  
    
    if no_day_between < 365:
        return getWeatherDataFromServer(begin_date,end_date)
    
    while no_day_between > YEAR_DURATION:

        tmp_data_get = getWeatherDataFromServer(
            new_date_retrieve,
            new_date_retrieve + timedelta(days=YEAR_DURATION)
        )
        
        ALL_DATA_RAIN_PERIOD = np.concatenate((ALL_DATA_RAIN_PERIOD, tmp_data_get))
        

        new_date_retrieve += timedelta(days=YEAR_DURATION)
        no_day_between -= YEAR_DURATION
    
    tmp_data_get = getWeatherDataFromServer(
        new_date_retrieve,
        new_date_retrieve + timedelta(days=no_day_between)
    )
    
    ALL_DATA_RAIN_PERIOD = np.concatenate((ALL_DATA_RAIN_PERIOD, tmp_data_get))
    
    return ALL_DATA_RAIN_PERIOD



    
def loadDataForPricing(file_name:str,start_date:date,end_date:date) -> np.ndarray: # cette fonction a pour but d'améliorer le temps d'exécution du pricing
    
    df_history_rain = pd.read_csv(file_name,sep=",")
    
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year = start_date.year
    year_pos = df_history_rain.columns.get_loc(str(year))
    day_since_begin_year = sum(days_in_month[:start_date.month - 1]) + start_date.day
    half_year = df_history_rain.iloc[day_since_begin_year:,year_pos].to_numpy()
    all_year = df_history_rain.iloc[:,(year_pos+1):].to_numpy().ravel()

    if (end_date < date.today()):
        data_remaining = []
    else:
        data_remaining = getHistoricalRainFallBetweenDates(date(2025,1,1),end_date)
        
    
    return np.concatenate([half_year,all_year,data_remaining])
   

