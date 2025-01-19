import requests
import json
import urllib.parse

def getWeatherDataForOneYear(begin_year:int, end_year:int):

    DAY_DURATION = 24
    DICT_EACH_YEAR = {}
    
    for year in range(begin_year, end_year):
        
        ALL_RAIN_DATA = []
    
        base_url = "https://www.infoclimat.fr/opendata/"
        params = {
            "version": "2", 
            "method": "get",
            "format": "json",  # use JSON format
            "stations[]": "07690",  # id of the Nice Weather Station
            "start": str(year)+"-01-01",  # begin date of the period
            "end": str(year)+"-12-31",  # end date of the period
            "token": "eZucxR2pA3oDfiWFlItshDc2Yzj9OIYSGevDhKtx9KZmkBjfedXQ"  # token
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
                    
                    # If pluie_1h is None or null, we replace it with 0
                    pluie_1h = data_in_hour.get("pluie_1h")
                    if pluie_1h is None:
                        pluie_1h = 0
                    
                    cum_rain_in_day = cum_rain_in_day + float(pluie_1h)
                    idx_24_hours = idx_24_hours + 1
                    
                    if idx_24_hours % DAY_DURATION == 0:  # we get 24 hours -> compute the average rain of the day
                        ALL_RAIN_DATA.append(cum_rain_in_day)  # append the cumulative rain of the day
                        idx_24_hours = 0  # reset to 0 for the next day
                        cum_rain_in_day = 0  # reset to 0 for the next day too
                
                DICT_EACH_YEAR[year] = ALL_RAIN_DATA.copy()
                ALL_RAIN_DATA.clear()
                print("Success: Data retrieved")
            else:
                print(f"Error: {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Error during requesting: {e}")
    
    return DICT_EACH_YEAR

DICT_FINAL = getWeatherDataForOneYear(2020, 2022)
print(DICT_FINAL.keys())
