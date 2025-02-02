# ACTUARIAL_PROJECT

## This project consists of a pricing of a weather insurance : the risk is the rain.

### See the paper on the code directly for more informations


# Note pour la compréhension : 

## L'interface étant jugée claire , nous laissons à l'utilisateur sa découverte. 
## Remarques pour les dévéloppeurs : 
    - Toutes les erreurs sont gérées automatiquement. 
    - Les entrèes de l'utilisateur sont vérifiées à chaque saisie.
    - L'optimisation des délais de requêtage ont été effectués seulement pour la ville de Nice - Côte d'Azur
        necéssitant une écriture en amont de l'historique de toute les données de pluviométries sur une période choisie du
        01/01/2004 au 01/12/2024. Ce choix est basé sur le fait que l'agence dans laquelle nous déployons le pricer est situé à Nice.
        Ainsi les calculs sont quasimenent instantanés. Cepandant, si le pricing s'effectue sur les données d'une ville différente,
        des temps de chargements sont à prévoir car le site infoclimat.fr étant un site open source, il est demandé au développeurs
        utilisant lurs données de ne pas dépasser un maximum de 5000 reqêuêtes en 24H. D'autre part, une requête ne peut récupérer les données que sur 365 jours d'ou les temps de chargement quand l'utilisateur décide de pricer sur une autre ville et une pétiode étendue. Nous laissons néanmoins ce choix à l'utilisateur final. 

## Concernant l'exécution de notre application : 
    - commencer par exécuter le requirements.txt (qui va donc installer toutes les dépendances de l'application)
    - récupérer votre adresse IPV4 sur ce site : https://ip.lafibre.info
    - générer ensuite la clé API sur ce site en renseignant votre adresse IPV4 (non commercial) : https://www.infoclimat.fr/opendata/
    - entrer la clé api dans le fichier key.txt
    - exécuter l'application en lançant la comande suivante : <streamlit run app.py>
    - Profitez de l'application

