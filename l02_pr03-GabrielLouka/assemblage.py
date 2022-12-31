from typing import List

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from constantes import DELTA_V_MINIMUM_PAR_CORPS_CELESTE, CHEMIN_CAPSULES, CHEMIN_MOTEURS, CHEMIN_RESERVOIRS
from fichiers_pieces import charger_capsules_df, charger_moteurs_df, charger_reservoirs_df
from fusee import Fusee, Capsule, Reservoir, Moteur


def creer_capsules(capsules_df: pd.DataFrame) -> List[Capsule]:
    # TODO Transformez le dataframe des capsules en liste d'objets de type Capsule
    liste_cap = []
    for pos_cap in range(len(capsules_df)):  #0, 1, 2, ...
        une_capsule = Capsule(capsules_df['nom'][pos_cap], capsules_df['hauteur'][pos_cap], capsules_df['masse'][pos_cap], capsules_df['prix'][pos_cap], capsules_df['places'][pos_cap])
        liste_cap.append(une_capsule)
    return liste_cap 


def creer_moteurs(moteurs_df: pd.DataFrame) -> List[Moteur]:
    # TODO Transformez le dataframe des moteurs en liste d'objets de type Moteur
    liste_mot = []
    for pos_mot in range(len(moteurs_df)):
        un_moteur = Moteur(moteurs_df['nom'][pos_mot], moteurs_df['hauteur'][pos_mot], moteurs_df['masse'][pos_mot], moteurs_df['prix'][pos_mot], moteurs_df['impulsion specifique'][pos_mot])
        liste_mot.append(un_moteur)
    return liste_mot 


def creer_reservoirs(reservoirs_df: pd.DataFrame) -> List[Reservoir]:
    # TODO Transformez le dataframe des reservoir en liste d'objets de type Reservoir
    liste_res = []
    for pos_res in range(len(reservoirs_df)):
        un_res = Reservoir(reservoirs_df['nom'][pos_res], reservoirs_df['hauteur'][pos_res], reservoirs_df['masse'][pos_res], reservoirs_df['prix'][pos_res], reservoirs_df['capacite'][pos_res])
        liste_res.append(un_res)
    return liste_res 


def corps_celestes_accessibles(fusee: Fusee) -> List[str]:
    # TODO Retournez la liste des corps célestes accessibles par la fusée.
    #  Utiliser DELTA_V_MINIMUM_PAR_CORPS_CELESTE
    list_planet = []
    print(fusee)
    for planet in DELTA_V_MINIMUM_PAR_CORPS_CELESTE.keys():
        if fusee.calculer_deltav() > DELTA_V_MINIMUM_PAR_CORPS_CELESTE[planet]:
            list_planet.append(planet)
    return list_planet


def comparer_fusee(fusee_1: Fusee, fusee_2: Fusee) -> None:
    # TODO créer un grouped barplot comparant les fusées passées en paramètre en fonction des trois métriques suivantes:
    #  * Masse / Coût
    h_m_1 = fusee_1.hauteur/fusee_1.masse
    h_m_2 = fusee_2.hauteur/fusee_2.masse
    #  * DeltaV / Coût
    dV_c_1 = fusee_1.calculer_deltav()/fusee_1.prix
    dV_c_2 = dV_c = fusee_2.calculer_deltav()/fusee_2.prix
    #  * DeltaV / Masse
    deltav_m1 = fusee_1.calculer_deltav()/fusee_1.masse
    deltav_m2 = fusee_2.calculer_deltav()/fusee_2.masse
    # TODO Générez un dataframe avec trois colonnes; fusée, résultats des différents ratios et type_ratio
    d1 = {'fusée': [fusee_1.nom, fusee_1.nom , fusee_1.nom], 'ratios': [deltav_m1, dV_c_1, h_m_1], 'type_ratio': ['deltaV/masse', 'deltaV/prix', 'hauteur/masse']}
    df_1 = pd.DataFrame(d1)
    d2 = {'fusée': [fusee_2.nom, fusee_2.nom, fusee_2.nom], 'ratios': [deltav_m2, dV_c_2, h_m_2], 'type_ratio': ['deltaV/masse', 'deltaV/prix', 'hauteur/masse']}
    df_2 = pd.DataFrame(d2)
    res=pd.concat([df_1, df_2])
    print(res)
    sns.barplot(x = 'fusée', y = 'ratios', data = res, hue = 'type_ratio').set(title=f'Comparaison de ratios de {fusee_1.nom} et {fusee_2.nom}')
    plt.show() 

if __name__ == '__main__':
    # creer_capsules
    capsules_df = charger_capsules_df(CHEMIN_CAPSULES)
    capsules = creer_capsules(capsules_df)
    for capsule in capsules:
        print(capsule)
    print()

    # creer_moteurs
    reservoirs_df = charger_moteurs_df(CHEMIN_MOTEURS)
    moteurs = creer_moteurs(reservoirs_df)
    for moteur in moteurs:
        print(moteur)
    print()

    # creer_reservoirs
    reservoirs_df = charger_reservoirs_df(CHEMIN_RESERVOIRS)
    reservoirs = creer_reservoirs(reservoirs_df)
    for reservoir in reservoirs:
        print(reservoir)
    print()

    # corps_celestes_accessibles
    capsule = Capsule("PasDBonSens", 1.5, 840.0, 600.0, 1)
    reservoir_1 = Reservoir("Piscine", 25.0, 9000.0, 13000.00, 6480.0)
    moteur = Moteur("La Puissance", 12.0, 15000.0, 39000.00, 295)
    fusee_1 = Fusee("Romano Fafard", capsule, reservoir_1, moteur)

    deltaV = fusee_1.calculer_deltav()
    corps_celestes = corps_celestes_accessibles(fusee_1)
    print(f"La fusée {fusee_1.nom} peut aller, avec {deltaV:.2f} de deltaV, jusqu'à: {corps_celestes}")
    print()

    # comparer_fusee
    reservoir_2 = Reservoir("Pichet", 0.4, 0.5, 20, 2)
    fusee_2 = Fusee("Romano Fafard Lite", capsule, reservoir_2, moteur)
    comparer_fusee(fusee_1, fusee_2)
