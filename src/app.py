#_______________ APP.PY _______________


import pandas as pd
import numpy as np
from formulas import getCA_pl_t, getR_pl_t
from load_data import *


# Example usage:
get_histo = False
if get_histo:
    writeHistoricalRainFallBetweenTwoYears(start_year=2004, end_year=2024, file_name="weather_data_by_year.csv")
df_weather_all_year = pd.read_csv("weather_data_by_year.csv")
df_final_weather = getWeatherTable(df_weather_all_year)
print(df_weather_all_year)


CA = 245
C_f = 10.0
pl_bar = 15.0
pl_t = df_final_weather.to_numpy()[:,0]
CA_pl_t = getCA_pl_t(CA,pl_bar,pl_t)
R_pl_t = getR_pl_t(CA,C_f,pl_bar,pl_t)
premium = np.mean(CA - CA_pl_t)


print(CA_pl_t)
print(premium)