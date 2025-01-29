# _______________ GUI.PY _______________

# GUI OF THE APPLICATION
from formulas import *
from load_data import *

from datetime import *
from dateutil.relativedelta import relativedelta

import streamlit as st
import pandas as pd




def initLaunchGui():
    # Conteneur principal
    with st.container():
        # Nettoyer et vérifier le chemin du fichier
        file_path = "./weather_data_by_year.csv"

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
                start_date = st.date_input("Date de début", date.today() - relativedelta(years=5), disabled=False)
                end_date = st.date_input("Date de fin", date.today(), disabled=False)
            else:
                st.info("L'historique des données n'est pas activé")
                start_date = st.date_input("Date de début", date.today() - relativedelta(years=5), disabled=True)
                end_date = st.date_input("Date de fin", date.today(), disabled=True)

            # Saisie des paramètres de tarification
            CA = st.number_input("Entrez le chiffre d'affaire journalier maximum (CA) en (€)", value=1000.00, step=1000.0)
            C_f = st.number_input("Entrez les coûts fixes (C_f) en (€)", value=100.00, step=10.0)
            pl_bar = st.number_input("Entrez le niveau de pluie pivot (pl_bar) en (mm)", value=10.00, step=0.50)
            launch_pricing = st.button("Lancez le pricing")

        # Vérifier si le premium a déjà été calculé
        if "premium" not in st.session_state:
            st.session_state.premium = None

        # Lancer le pricing si le bouton est pressé
        if launch_pricing:
            with st.container():
                # Si l'historique des données est demandé, effectuer les calculs et afficher les résultats

                pl_t = loadDataForPricing("weather_data_by_year.csv",start_date,end_date)
                R_pl_t = getR_pl_t(CA, C_f, pl_bar, pl_t)
                premium = getPremium(R_pl_t,round(float(((end_date-start_date).days)/365),2))

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

                # Logique du benchmark
                a, b, c = getBenchmark(benchmark_start_date, CA, C_f, pl_bar,((end_date - start_date)/365).days)
                
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
