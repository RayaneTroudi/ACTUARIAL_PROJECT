# _______________ FORMULAS.PY _______________
# CONTAINS ALL THE FUNCTIONS NEEDED TO COMPUTE PREMIUM AND OTHERS PARAMETERS
import numpy as np
from load_data import *


# -------------------------------------------------------------------------------------------------- #

def getR_pl_t(CA:float, C_f:float, pl_bar:float,pl_t:np.array) -> np.array:
    """this function compute the result of the company 

    Args:
        CA (float): Maximum turnover of the company during a day
        C_f (float): Maximum Fixed Cost during a day
        pl_bar (float): Pivot rain level 
        pl_t (np.array): level of rain by day in mm

    Returns:
        np.array: result of the company each day
    """
    
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

# -------------------------------------------------------------------------------------------------- #


def getPremium(R_pl_t:np.array,years:float) -> float:
    """

    Args:
        R_pl_t (np.array): Result of the company at each day of the period studying
        years (float): time period in years 

    Returns:
        float: the premium of the insurance
    """

    return round(np.sum(np.abs(R_pl_t[R_pl_t < 0])) / years,2)

# -------------------------------------------------------------------------------------------------- #


def getAllLoses(R_pl_t:np.array) -> np.array:
    
    return np.sum(np.abs(R_pl_t[R_pl_t <= 0]))

# -------------------------------------------------------------------------------------------------- #


def getRWithLosesWithInsurance(R_pl_t:np.array,years:int) -> float :
    """

    Args:
        R_pl_t (np.array): Result of the company at each day of the period studying
        years (int): time period in years 

    Returns:
        np.array: all the loses during the period
    """
    return getAllLoses(R_pl_t) + np.sum(R_pl_t[R_pl_t > 0]) - getPremium(R_pl_t,years)


# -------------------------------------------------------------------------------------------------- #



def getRWithLosesWithoutInsurance(R_pl_t:np.array) -> float:
    """

    Args:
        R_pl_t (np.array): Result of the company at each day of the period studying

    Returns:
        np.array: all the loses during the period
    """
    return np.sum(R_pl_t)


# -------------------------------------------------------------------------------------------------- #


def getBenchmark(year:int,CA:float,C_f:float,pl_bar:float,years:int,id_city:str):
    
    array_year_rain = np.array(getWeatherDataFromServer(date(year,1,1),date(year,12,31),id_city))
    R_pl_t_year = getR_pl_t(CA,C_f,pl_bar,array_year_rain)
    return getAllLoses(R_pl_t_year),getRWithLosesWithInsurance(R_pl_t_year,years),getRWithLosesWithoutInsurance(R_pl_t_year)

# -------------------------------------------------------------------------------------------------- #



    
    