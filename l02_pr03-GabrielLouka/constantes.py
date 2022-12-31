CHEMIN_PIECES = "donnees_pieces" 
CHEMIN_CAPSULES = CHEMIN_PIECES + "/capsules"
CHEMIN_MOTEURS = CHEMIN_PIECES + "/moteurs"
CHEMIN_RESERVOIRS = CHEMIN_PIECES + "/reservoirs"

FICHIER_CAPSULE = "capsules.csv"
FICHIERS_RESERVOIRS = ["reservoir1.json", "reservoir2.json", "reservoir3.json"]
FICHIERS_MOTEURS = ["moteur1.ppl", "moteur2.ppl", "moteur3.ppl", "moteur4.ppl"]

IMPULSION_SPECIFIQUE_MINIMALE = 200  # En s

MASSE_VOLUMIQUE_CARBURANT = 50.0  # En kg/l
CHAMP_GRAVITATIONNEL = 9.81  # En m/s^2

# Inspiré par https://www.deltacalculator.com
DELTA_V_MINIMUM_PAR_CORPS_CELESTE = {
    'Mercure': 8361,
    'Vénus': 4501,
    'Mars': 4711,
    'Jupiter': 5471,
    'Saturn': 5969,
    'Uranus': 6467,
    'Neptune': 6965,
    'Pluton': 7461
}
