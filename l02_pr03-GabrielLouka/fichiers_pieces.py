from numpy.core.fromnumeric import shape
import pandas as pd
import os
import numpy as np
from pandas.core.frame import DataFrame
from pandas.core.resample import f

 
from constantes import CHEMIN_CAPSULES, CHEMIN_MOTEURS, CHEMIN_RESERVOIRS, FICHIER_CAPSULE, FICHIERS_RESERVOIRS, \
    FICHIERS_MOTEURS
 
 
def charger_capsules_df(chemin_capsules: str) -> pd.DataFrame:
    # TODO Retournez un dataframe des capsules décrites dans le fichier FICHIER_CAPSULE
    #  Il faut aussi renommer les colonnes pour que celles-ci soient plus lisibles
    capsule_df = pd.read_csv(os.path.join(chemin_capsules, FICHIER_CAPSULE))
    final_df = capsule_df.rename(columns={'n':'nom', 'h':'hauteur', 'm':'masse', 'p':'prix', 'pl':'places'})
    return final_df
 

def charger_reservoirs_df(chemin_reservoirs: str) -> pd.DataFrame:
    # TODO Retournez un dataframe combiné des réservoirs décrits dans
    #  les fichiers FICHIERS_RESERVOIRS
    lis = []
    for index_file in range(len(FICHIERS_RESERVOIRS)):
        sub_df_1 = pd.read_json(os.path.join(chemin_reservoirs, FICHIERS_RESERVOIRS[index_file]))
        lis.append(sub_df_1)
        res_df = pd.concat(lis)

    return res_df.reset_index(drop=True) 


def charger_moteurs_df(chemin_moteurs: str) -> pd.DataFrame:
    # TODO Retournez un dataframe combiné des moteurs décrits dans
    #  les fichiers FICHIERS_MOTEURS
    list_fil = []
    for index2_file in range(len(FICHIERS_MOTEURS)):
        with open(os.path.join(chemin_moteurs, FICHIERS_MOTEURS[index2_file])) as mot_file:
            liste_col = []
            liste_row = []
            for line in mot_file:
                if line == "\n" or line.startswith('#'):
                    continue
                else:
                    liste_col.append(line.split('=', 2)[0])
                    liste_row.append(line.split('=', 2)[1].replace('\n', '')) #replace car il y avait un soucis lors du split et append dans le df
                    moteur_df = pd.DataFrame([liste_row], columns=liste_col)
            list_fil.append(moteur_df)
            moteur_df_final = pd.concat(list_fil).reset_index(drop=True)
    moteur_df_final = moteur_df_final.astype({"nom": str, "hauteur": float, "masse": float, "prix": float, "impulsion specifique": np.int64})
    return moteur_df_final


def filtrer_moteurs(moteurs_df: pd.DataFrame, impulsion_minimum: int) -> pd.DataFrame:
    # TODO Retourner un sous-ensemble filtré d'un df de moteurs
    #  où l'impulsion spécifique est au dessus d'un certain seuil
    filt_eng = moteurs_df.loc[moteurs_df["impulsion specifique"] > impulsion_minimum]
    return filt_eng


if __name__ == '__main__':
    # charger_capsules_df
    capsules = charger_capsules_df(CHEMIN_CAPSULES)
    print(capsules)
    print()

    # charger_reservoirs_df
    reservoirs = charger_reservoirs_df(CHEMIN_RESERVOIRS)
    print(reservoirs)
    print()

    # charger_moteurs_df
    moteurs = charger_moteurs_df(CHEMIN_MOTEURS)
    print(moteurs)
    print()

    # filtrer_moteurs
    moteurs_filtres = filtrer_moteurs(moteurs, 220)
    print(moteurs_filtres)
