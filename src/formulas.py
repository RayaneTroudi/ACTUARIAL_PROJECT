# _______________ FORMULAS.PY _______________

import numpy as np


def getCA_pl_t(CA:float,pl_bar:float,pl_t:np.array) -> np.array:
    
    CA_pl_t = np.zeros_like(pl_t)
   
    cd_1 = (pl_t > pl_bar)
    CA_pl_t[cd_1] = 0
    
    cd_2 = (pl_t > 0) & (pl_t < pl_bar)
    f_pl_t = ( pl_bar - pl_t[cd_2] ) / pl_bar
    CA_pl_t[cd_2] = f_pl_t * CA
    
    cd_3 = (pl_t == 0) 
    f_pl_t = ( pl_bar - pl_t[cd_3] ) / pl_bar
    CA_pl_t[cd_3] = CA
    
    return CA_pl_t



def getR_pl_t(CA:float, C_f:float, pl_bar:float,pl_t:np.array) -> np.array:
    
    R_pl_t = np.zeros_like(pl_t)
   
    cd_1 = (pl_t > pl_bar)
    R_pl_t[cd_1] = - C_f
    
    cd_2 = (pl_t > 0) & (pl_t < pl_bar)
    f_pl_t = ( pl_bar - pl_t[cd_2] ) / pl_bar
    R_pl_t[cd_2] = f_pl_t * CA - C_f
    
    cd_3 = (pl_t == 0) 
    f_pl_t = ( pl_bar - pl_t[cd_3] ) / pl_bar
    R_pl_t[cd_3] = CA - C_f
    
    return R_pl_t