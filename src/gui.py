# _______________ GUI.PY _______________
# GUI OF THE APPLICATION

from formulas import *
from load_data import *
from pdf_generator import *

from datetime import *
from dateutil.relativedelta import relativedelta

import streamlit as st
import pandas as pd
import os


# -------------------------------------------------------------------------------------------------- #


def initLaunchGui():
 
    with st.container():
        
        # Conteneur de saisie des paramètres
        with st.container():
            st.info("La profondeur maximale d'historique est de 20 années (01/01/2024)")
            get_history = st.checkbox("Voulez-vous modifier la profondeur de la simulation?")

            if get_history:
                start_date = st.date_input("Date de début", date.today() - relativedelta(years=5), disabled=False, min_value=date(2004, 1, 1))
                end_date = st.date_input("Date de fin", date.today(), disabled=False)
            else:
                start_date = st.date_input("Date de début", date.today() - relativedelta(years=5), disabled=True, min_value=date(2004, 1, 1))
                end_date = st.date_input("Date de fin", date.today(), disabled=True)

            if (end_date.year - start_date.year == 0):
                st.info(f"Le calcul du pricing est réglé sur moins d'un an")
            else:
                st.info(f"Le calcul du pricing est réglé sur les {end_date.year - start_date.year} dernières années")

            # input to get the parameters of the pricing
            CA = st.number_input("Entrez le chiffre d'affaire journalier maximum (CA) en (€)", value=1000.00, step=1000.0)
            C_f = st.number_input("Entrez les coûts fixes (C_f) en (€)", value=100.00, step=10.0)
            pl_bar = st.number_input("Entrez le niveau de pluie pivot (pl_bar) en (mm)", value=10.00, step=0.50)

        # check if the premium is already compute
        if "premium" not in st.session_state:
            st.session_state.premium = None

        # inform the user that the history is set to 2004 at maximum of depth
        if start_date > date(2004, 1, 1):
            launch_pricing = st.button("Lancez le pricing")

            # launch the pricing
            if launch_pricing:
                with st.container():
                    # load the data
                    pl_t = loadDataForPricing("weather_data_by_year.csv", start_date, end_date)
                    R_pl_t = getR_pl_t(CA, C_f, pl_bar, pl_t)
                    premium = getPremium(R_pl_t, round(float(((end_date - start_date).days) / 365), 2))

                    # stock the premium because streamlit refresh the page at each click on a element of the page
                    st.session_state.premium = premium

                    # disp the premium
                    st.write(f"Premium Pur (sans marge) : {st.session_state.premium:.2f} €")

            # input for the benchmark
            benchmark_start_date = st.number_input("Année du benchmark", value=2024, step=1)

            # check if the pricing is done before starting the benchmark
            if st.session_state.premium is not None:
                benchmark_button = st.button("Lancer le benchmark")

                if benchmark_button:
                    # launch the benchmark
                    lost, res_with_insurance, res_without_insurance = getBenchmark(benchmark_start_date, CA, C_f, pl_bar, ((end_date - start_date) / 365).days)

                    # Stocker les résultats du benchmark
                    st.session_state.benchmark_results = (lost, res_with_insurance, res_without_insurance)

                    # Affichage des résultats
                    st.subheader(f"Résultat du benchmark sur l'année {benchmark_start_date}")
                    st.write(f"Premium (€) = {round(st.session_state.premium, 2)}")
                    st.write(f"Pertes (€) = {round(lost, 2)}")
                    st.write(f"Résultat avec assurance (€) = {round(res_with_insurance, 2)}")
                    st.write(f"Résultat sans assurance (€) = {round(res_without_insurance, 2)}")
                    st.info(" ✅ Votre devis a été généré avec succès.")

                    # pdf generation
                    pdf_filename = "devis.pdf"
                    getPdf(pdf_filename, 
                           st.session_state.premium, 
                           lost, res_with_insurance, 
                           res_without_insurance, 
                           pl_bar, 
                           C_f, 
                           CA, 
                           start_date, 
                           end_date, 
                           benchmark_start_date)

                    # check verification and set button download
                    if os.path.exists(pdf_filename):
                        st.success("✅ PDF généré avec succès !")

                        # read the file
                        with open(pdf_filename, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()

                        # download button
                        st.download_button(
                            label="📥 Télécharger le PDF",
                            data=pdf_bytes,
                            file_name=pdf_filename,
                            mime="application/pdf"
                        )
                    else:
                        st.error("🚨 Fichier PDF non trouvé ! Vérifiez s'il a bien été généré.")

            else:
                st.info("Veuillez d'abord lancer le pricing avant de pouvoir effectuer le benchmark.")
        else:
            st.warning("⚠️ Veuillez saisir une date supérieure au 01/01/2004.")

