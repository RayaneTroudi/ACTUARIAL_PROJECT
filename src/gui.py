# _______________ GUI.PY _______________

from formulas import *
from load_data import *

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import io


# Nettoyer et vérifier le chemin du fichier
file_path = "./weather_data_by_year.csv"
print(repr(file_path))  # Afficher le chemin pour vérifier s'il contient des caractères invisibles.

# Lire le fichier CSV
try:
    df_weather_all_year = pd.read_csv(file_path)
except OSError as e:
    st.error(f"Erreur lors de la lecture du fichier : {e}")
    st.stop()

# Saisie des paramètres de tarification
get_history = st.checkbox("Voulez-vous récuperer un historique de données ?")

if get_history:
    
    start_date = st.date_input("Date de début", datetime(2004, 1, 1),disabled=False)
    end_date = st.date_input("Date de fin", datetime(2024, 1, 1),disabled=False)
    st.write(f"Période sélectionnée : {start_date} au {end_date}")

else:
    st.info("L'historique des données n'est pas activé")
    start_date = st.date_input("Date de début", datetime(2004, 1, 1),disabled=True)
    end_date = st.date_input("Date de fin", datetime(2024, 1, 1),disabled=True)
    
 
CA = st.number_input("Entrez le chiffre d'affaire journalier maximum (CA) en (€)", value=90000.0, step=1000.0)
C_f = st.number_input("Entrez les coûts fixes (C_f) en (€)", value=10.0, step=1.0)
pl_bar = st.number_input("Entrez le niveau de pluie pivot (pl_bar) en (mm)", value=15.0, step=1.0)
launch_pricing = st.button("Lancez le pricing")


if launch_pricing:
    
    if get_history: # we want to get an history of data
        
        output_placeholder = st.empty()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        writeHistoricalRainFallBetweenTwoYears(start_year=int(start_date.strftime('%Y')), end_year=int(end_date.strftime('%Y')), file_name="weather_data_by_year.csv")
        sys.stdout = sys.__stdout__
        output_placeholder.text(captured_output.getvalue()+"\n")

        
    df_weather_all_year = pd.read_csv("weather_data_by_year.csv")
    df_final_weather = getWeatherTable(df_weather_all_year)
    pl_t = df_final_weather.to_numpy()[:,0]
    CA_pl_t = getCA_pl_t(CA,pl_bar,pl_t)
    R_pl_t = getR_pl_t(CA,C_f,pl_bar,pl_t)
    premium = np.mean(CA - CA_pl_t)
    
    
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Récupère la première ligne (les en-têtes)

    # Affichage des résultats
    st.subheader("Paramètres du pricing : ")
    # Affichage avec les unités à côté des valeurs saisies
    st.write(f"CA = {CA} €")
    st.write(f"C_f = {C_f} €")
    st.write(f"pl_bar = {pl_bar} mm")
    st.write(f"begin_year = {headers[0]} ")
    st.write(f"end_year = {headers[len(headers)-1]}")

    st.subheader("Résultats du pricing : ")
    st.write(f"Premium Pur : {premium:.2f} €")





