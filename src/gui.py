# _______________ GUI.PY _______________

from formulas import *
from load_data import *

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import io


def initLaunchGui():
    # Conteneur principal
    with st.container():
        # Nettoyer et vérifier le chemin du fichier
        file_path = "./weather_data_by_year.csv"
        print(repr(file_path))  # Afficher le chemin pour vérifier s'il contient des caractères invisibles.

        # Lire le fichier CSV
        try:
            df_weather_all_year = pd.read_csv(file_path)
        except OSError as e:
            st.error(f"Erreur lors de la lecture du fichier : {e}")
            st.stop()

        # Conteneur de saisie des paramètres
        with st.container():
            st.info("Par défaut, la profondeur de simulation est de 5 ans à partir de la date actuelle J, jour du pricing")
            get_history = st.checkbox("Voulez-vous modifier la profondeur de la simulation?")
            
            if get_history:
                start_date = st.date_input("Date de début", datetime(2004, 1, 1), disabled=False)
                end_date = st.date_input("Date de fin", datetime(2024, 1, 1), disabled=False)
            else:
                st.info("L'historique des données n'est pas activé")
                start_date = st.date_input("Date de début", datetime(2004, 1, 1), disabled=True)
                end_date = st.date_input("Date de fin", datetime(2024, 1, 1), disabled=True)

            # Saisie des paramètres de tarification
            CA = st.number_input("Entrez le chiffre d'affaire journalier maximum (CA) en (€)", value=1000.00, step=1000.0)
            C_f = st.number_input("Entrez les coûts fixes (C_f) en (€)", value=500.00, step=1.0)
            pl_bar = st.number_input("Entrez le niveau de pluie pivot (pl_bar) en (mm)", value=15.00, step=1.0)
            launch_pricing = st.button("Lancez le pricing")

        # Vérifier si le premium a déjà été calculé
        if "premium" not in st.session_state:
            st.session_state.premium = None

        # Lancer le pricing si le bouton est pressé
        if launch_pricing:
            with st.container():
                # Si l'historique des données est demandé, effectuer les calculs et afficher les résultats
                if get_history:
                    output_placeholder = st.empty()
                    captured_output = io.StringIO()
                    sys.stdout = captured_output
                    writeHistoricalRainFallBetweenTwoYears(start_year=int(start_date.strftime('%Y')), end_year=int(end_date.strftime('%Y')), file_name="weather_data_by_year.csv")
                    sys.stdout = sys.__stdout__
                    output_placeholder.text(captured_output.getvalue() + "\n")

                # Recalculer les valeurs pour le pricing
                df_weather_all_year = pd.read_csv("weather_data_by_year.csv")
                pl_t = getWeatherTable(df_weather_all_year)
                R_pl_t = getR_pl_t(CA, C_f, pl_bar, pl_t)
                premium = getPremium(R_pl_t)

                # Mettre à jour le premium dans st.session_state avec la nouvelle valeur calculée
                st.session_state.premium = premium

                # Afficher la nouvelle valeur du premium calculé
                st.write(f"Premium recalculé : {st.session_state.premium:.2f} €")

        # Saisie de l'année du benchmark avant de cliquer sur le bouton
        benchmark_start_date = st.number_input("Année du benchmark", value=2024, step=1)

        # Vérifier si le pricing a été lancé avant d'afficher le bouton de benchmark
        if st.session_state.premium is not None:
            # Ajout d'un bouton pour lancer le benchmark
            benchmark_button = st.button("Lancer le benchmark")

            # Si le bouton benchmark est pressé, lancer les calculs
            if benchmark_button:
                print("ici")
                print(st.session_state.premium)
                # Logique du benchmark
                a, b, c = getBenchmark(benchmark_start_date, st.session_state.premium, CA, C_f, pl_bar)
                
                # Stocker les résultats du benchmark
                st.session_state.benchmark_results = (a, b, c)

                # Affichage des résultats du benchmark
                st.subheader(f"Résultat du benchmark sur l'année {benchmark_start_date}")
                st.write(f"Premium (€) = {round(st.session_state.premium, 2)}")
                st.write(f"Pertes (€) = {round(a, 2)}")
                st.write(f"Résultat avec assurance (€) = {round(b, 2)}")
                st.write(f"Résultat sans assurance (€) = {round(c, 2)}")
        else:
            st.info("Veuillez d'abord lancer le pricing avant de pouvoir effectuer le benchmark.")
