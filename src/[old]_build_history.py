# _______________ LOAD_DATA.PY _______________

# THIS FILE CONSISTS TO BUILD AND HISTORY OF RAIN DATA AND STOCK IT IN THE FILE <weather_data_by_year.csv>
# IT'S NEVER USED BY THE APPLICATION EXCEPTS THE DEVELOPPER ITSELF BY COMMAND LINE TO BUILD A NEW HISTORY
# BY DEFAULT WE LOAD DATA RAIN BETWEEN 2004-01-01 AND 2024-12-31.
# DATA AFTER THIS TIME INTERVAL ARE LOADED BY FUNCTIONS IN THE FILE <load_data.py> FOR REAL-TIME UPDATE

import requests
import urllib.parse
import csv
import pandas as pd

def getWeatherDataForOneYear(begin_year: int,id_station:str):
    """
    Fetch weather data for a single year.
    """
    DAY_DURATION = 24
    ALL_RAIN_DATA = []

    base_url = "https://www.infoclimat.fr/opendata/"
    params = {
        "version": "2",
        "method": "get",
        "format": "json",
        "stations[]": id_station,
        "start": f"{begin_year}-01-01",
        "end": f"{begin_year}-12-31",
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

            for data_in_hour in data["hourly"][id_station]:
                pluie_1h = data_in_hour.get("pluie_1h", 0) or 0
                cum_rain_in_day += float(pluie_1h)
                idx_24_hours += 1

                if idx_24_hours % DAY_DURATION == 0:
                    ALL_RAIN_DATA.append(round(cum_rain_in_day, 1))
                    cum_rain_in_day = 0
                    idx_24_hours = 0

            print(f"Success: Data retrieved for year {begin_year}")
        else:
            print(f"Error: {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error during request: {e}")

    return ALL_RAIN_DATA


def getHistoricalRainFallBetweenTwoYears(start_year: int, end_year: int):
    """
    Fetch historical rainfall data for a range of years.
    """
    DICT_HISTORICAL_DATA_RAIN = {}

    for year in range(start_year, end_year + 1):
        rain_year_tmp = getWeatherDataForOneYear(year)
        DICT_HISTORICAL_DATA_RAIN[year] = rain_year_tmp

    return DICT_HISTORICAL_DATA_RAIN


def writeHistoricalRainFallBetweenTwoYears(start_year: int, end_year: int, file_name: str):
    """
    Write historical rainfall data for a range of years to a CSV file.
    """
    # Fetch historical rainfall data
    historical_data = getHistoricalRainFallBetweenTwoYears(start_year, end_year)

    # Open the CSV file in write mode
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row with years
        header = [str(year) for year in range(start_year, end_year + 1)]
        writer.writerow(header)

        # Determine the maximum number of days (assuming 365 days per year)
        num_days = 365

        # Write the data row by row for each day
        for day in range(num_days):
            row = [day + 1]  # Day number starts at 1
            for year in range(start_year, end_year + 1):
                # Append the rainfall data for each year (use 0 if data is missing)
                rainfall = historical_data.get(year, [])
                row.append(rainfall[day] if day < len(rainfall) else 0)

            # Write the row to the CSV file
            writer.writerow(row)

    print(f"Historical rainfall data for {start_year} to {end_year} written to {file_name}")

def getWeatherTable(df_all_years:pd.DataFrame) -> pd.DataFrame:
    
    df_final = pd.DataFrame()
    df_final["Rain_in_mm"] = df_all_years.sum(axis=1)
    df_final["Rain_in_mm"] = round(df_final["Rain_in_mm"] / len(df_all_years.columns),1)
    
    return df_final
    
    
# BY DEFAULT WE USE A TIME PERIOD OF 20 YEARS BETWEEN 2004 AND 2024
writeHistoricalRainFallBetweenTwoYears(2000,2024,"./weather_data_by_year")   
    
    
    