# _______________ LOAD_DATA.PY _______________

# CONTAINS ALL FUNCTION TO GET DATA BETWEEN TWO DATE 
# THIS FILE USE THE CSV HISTORY FOR BETTER PERFORMANCE
# AND GET NEW DATA IN REAL-TIME

import requests
import urllib.parse
import pandas as pd
import numpy as np

from datetime import date, timedelta
from InfoClimatAPI import InfoClimat

# -------------------------------------------------------------------------------------------------- #


def getWeatherDataFromServer(begin_date:date,end_date:date,id_city:str) -> np.array:

    """This function get the rain data day by day in a MAXIMUM of 365 days by request (due to the general uses conditions of the site)

    Raises:
        ValueError: beyond one year of data

    Returns:
        (np.array): an array that contains all level of rain of each day during at a maximum of 365 days
    """
    
    DAY_DURATION = 24
    YEAR_DURATION = 365
    ALL_RAIN_DATA = []

    if ((end_date-begin_date).days) > YEAR_DURATION:
        raise ValueError("Attention l'écart entre les deux dates dépassent 1 an")

    base_url = "https://www.infoclimat.fr/opendata/"
    token = getTokenInFile("./token.txt")
    print(token)
    # parameters of the request
    params = {
        "version": "2",
        "method": "get",
        "format": "json",
        "stations[]": id_city,
        "start": begin_date.strftime("%Y-%m-%d"),
        "end": end_date.strftime("%Y-%m-%d"), # AAAA-MM-DD
        "token": token,
    }

    query_string = "&".join([f"{key}={urllib.parse.quote(str(value))}" for key, value in params.items()])
    API_URL = f"{base_url}?{query_string}"

    # launch the request
    try:
        response = requests.get(API_URL)

        if response.status_code == 200:
            data = response.json()
     
            cum_rain_in_day = 0
            idx_24_hours = 0

            for data_in_hour in data["hourly"][id_city]:
                pluie_1h = data_in_hour.get("pluie_1h", 0) or 0
                
                # cumulate rain hour by hour
                cum_rain_in_day += float(pluie_1h)
                idx_24_hours += 1

                # a day is passed 
                if idx_24_hours % DAY_DURATION == 0:
                    ALL_RAIN_DATA.append(round(cum_rain_in_day, 1))
                    cum_rain_in_day = 0
                    idx_24_hours = 0

            print(f"Success: Data retrieved for year period {begin_date} to {end_date}")
        else:
            print(f"Error: {response.status_code}: {response.text}")
            return []
    except Exception as e:
        print(f"Error during request: {e}")

    return ALL_RAIN_DATA

# -------------------------------------------------------------------------------------------------- #



def getHistoricalRainFallBetweenDates(begin_date: date, end_date: date, id_city:str):
    
    """This function is an extension of the first one, the difference is that you can chosse date dates where 
       the difference between them are greater than 365 days

    """

    YEAR_DURATION = 365  
    no_day_between = (end_date - begin_date).days
    
    if no_day_between <= 0:
        raise ValueError("La date de début doit être antérieure à la date de fin.")
    
    new_date_retrieve = begin_date
    # initializing the numpy array
    ALL_DATA_RAIN_PERIOD = np.array([])  
    
    # duration < 365 call the first function
    if no_day_between < YEAR_DURATION:
        return getWeatherDataFromServer(begin_date,end_date,id_city)
    
    # > 365 call several times the first function to do not break the rule of the site (1 request of 365 days at maximum)
    while no_day_between > YEAR_DURATION:

        tmp_data_get = getWeatherDataFromServer(
            new_date_retrieve,
            new_date_retrieve + timedelta(days=YEAR_DURATION),
            id_city
        )
        
        # concatenate the array
        ALL_DATA_RAIN_PERIOD = np.concatenate((ALL_DATA_RAIN_PERIOD, tmp_data_get))
        

        new_date_retrieve += timedelta(days=YEAR_DURATION)
        no_day_between -= YEAR_DURATION
    
    # last call at the end of the while
    tmp_data_get = getWeatherDataFromServer(
        new_date_retrieve,
        new_date_retrieve + timedelta(days=no_day_between),
        id_city
    )
    
    # return the data containing rain level during a period 
    ALL_DATA_RAIN_PERIOD = np.concatenate((ALL_DATA_RAIN_PERIOD, tmp_data_get))
    
    return ALL_DATA_RAIN_PERIOD

# -------------------------------------------------------------------------------------------------- #


    
def loadDataForPricing(file_name:str,start_date:date,end_date:date,id_city:str) -> np.ndarray: 
    """This function aims to improve the execution time of the application by use an history of level rain data that build
       before the execution manually by us. This historic have a depth of 20 years by default.
       You can change this history by launch manually the fild starting by <[old] ... > see the comment in this file 
       for more informations.

    Args:
        file_name (str): file name of the history
        start_date (date): start date that you want to get the level rain data
        end_date (date): end date that you want to get the level rain data

    Returns:
        np.ndarray: an array that contains all data rain level by day during the period
    """
    if (id_city == "07690"):
        df_history_rain = pd.read_csv(file_name,sep=",")
        
        MAX_YEAR_HISTORY = 2024
        
        # leap year is ignored
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        year = start_date.year
        year_pos = df_history_rain.columns.get_loc(str(year))

        # get the data from the history by reading him
        day_since_begin_year = sum(days_in_month[:start_date.month - 1]) + start_date.day - 1
        half_year = df_history_rain.iloc[day_since_begin_year:,year_pos].to_numpy()

        if (date.today().year  < MAX_YEAR_HISTORY ):
            end_year_pos = df_history_rain.columns.get_loc(str(end_date.year))
            all_year = df_history_rain.iloc[:,(year_pos):end_year_pos].to_numpy().ravel()
        else:
            all_year = df_history_rain.iloc[:,(year_pos):23].to_numpy().ravel()

        # get the data that are not present in the history (because the history contains data since 31/12/2024) in real-time
        if (end_date < date.today()):
            data_remaining = []
        else:
            data_remaining = getHistoricalRainFallBetweenDates(date(2025,1,1),end_date,id_city)
            
        return np.concatenate([half_year,all_year,data_remaining])
            
    else:
        return getHistoricalRainFallBetweenDates(date(2020,1,1),end_date,id_city)
        
            

    
   
# -------------------------------------------------------------------------------------------------- #

def getCityAvailable() -> dict:
    
    API = InfoClimat()
    
    stations = API.get_stations()
    STATION_BY_ID_AND_CITY = dict()

    if stations:
        for station in stations:
            station_id = station.get('id', 'N/A')
            ville = station.get('libelle', 'Inconnue') 
            STATION_BY_ID_AND_CITY[ville] = station_id
            
    else:
        raise ValueError("Aucune Station n'a été retournée par la requête")
    
    return STATION_BY_ID_AND_CITY


# -------------------------------------------------------------------------------------------------- #


def getTokenInFile(file_name:str) -> str:

    with open(file_name, "r", encoding="utf-8") as f:
        token = f.read().strip()  

    return token

