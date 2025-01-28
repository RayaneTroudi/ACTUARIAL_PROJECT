# _______________ FORMULAS.PY _______________

import numpy as np
from load_data import *

def getR_pl_t(CA:float, C_f:float, pl_bar:float,pl_t:np.array) -> np.array:
    
    R_pl_t = np.zeros_like(pl_t)
   
    cd_1 = (pl_t >= pl_bar)
    R_pl_t[cd_1] = - C_f
    
    cd_2 = (pl_t > 0) & (pl_t < pl_bar)
    f_pl_t = ( pl_bar - pl_t[cd_2] ) / pl_bar
    R_pl_t[cd_2] = (f_pl_t * CA) - C_f
    
    cd_3 = (pl_t == 0) 
    f_pl_t = ( pl_bar - pl_t[cd_3] ) / pl_bar
    R_pl_t[cd_3] = CA - C_f
    
    return R_pl_t


def getPremium(R_pl_t:np.array) -> np.array:
    
    return np.mean(np.abs(R_pl_t[R_pl_t <= 0]))

def getAllLoses(R_pl_t:np.array) -> np.array:
    
    return np.sum(np.abs(R_pl_t[R_pl_t <= 0]))

def getRWithLosesWithInsurance(R_pl_t:np.array) -> np.array :
    
    return getAllLoses(R_pl_t) + np.sum(R_pl_t[R_pl_t > 0]) - getPremium(R_pl_t)

def getRWithLosesWithoutInsurance(R_pl_t:np.array) -> np.array:
    
    return np.sum(R_pl_t)


def getBenchmark(year:int,premium:float,CA:float,C_f:float,pl_bar:float):
    
    array_year_rain = np.array(getWeatherDataForOneYear(year))
    R_pl_t_year = getR_pl_t(CA,C_f,pl_bar,array_year_rain)
    return getAllLoses(R_pl_t_year),getRWithLosesWithInsurance(R_pl_t_year),getRWithLosesWithoutInsurance(R_pl_t_year)
    # pertes, resultat avec assurance, resultat sans assurance
    
    
    