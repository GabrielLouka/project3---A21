from typing import Tuple

from assemblage import creer_capsules, creer_reservoirs, creer_moteurs, corps_celestes_accessibles, comparer_fusee
from constantes import IMPULSION_SPECIFIQUE_MINIMALE, CHEMIN_CAPSULES, CHEMIN_RESERVOIRS, CHEMIN_MOTEURS
from fichiers_pieces import charger_capsules_df, charger_reservoirs_df, charger_moteurs_df, filtrer_moteurs
from fusee import Fusee


def main() -> Tuple[Fusee, Fusee]:
    # Pièces
    # Chargement des pièces
    capsules_df = charger_capsules_df(CHEMIN_CAPSULES)
    reservoirs_df = charger_reservoirs_df(CHEMIN_RESERVOIRS)
    moteurs_df = charger_moteurs_df(CHEMIN_MOTEURS)

    # TODO Filtrez les moteurs avec une impulsion spécifique plus
    #  petite que IMPULSION_SPECIFIQUE_MINIMALE
    moteur_filtres = filtrer_moteurs(moteurs_df, IMPULSION_SPECIFIQUE_MINIMALE).reset_index(drop=True)
    # TODO Affichez (print) les trois dataframes
    print(capsules_df)
    print(reservoirs_df)
    print(moteur_filtres)
    # Assemblage
    # TODO Créez des objets de type Capsule, Reservoir et Moteur
    #  à partir des dataframes
    cap = creer_capsules(capsules_df)    
    res = creer_reservoirs(reservoirs_df)
    mot = creer_moteurs(moteur_filtres)
    # TODO Créez deux fusées
    fusees = []
    for i in range(2):
        nom_fusee = input("Veuillez entrer le nom de la fusée : ")
        index_capsule = int(input("Veuillez entrer le numéro de la capsule désirée : "))
        index_reservoir = int(input("Veuillez entrer le numéro du réservoir désiré : "))
        index_moteur = int(input("Veuillez entrer le numéro du moteur désiré : "))
        # TODO Créer une fusée à partir des pièces choisies et ajoutez la à la liste fusees
        une_fusee = Fusee(nom_fusee, cap[index_capsule], res[index_reservoir], mot[index_moteur])
        fusees.append(une_fusee)
        # TODO Afficher (print) la fusée
        print(une_fusee)
        

    # Comparaison
    # TODO Affichez les corps célestes accessibles par les deux fusées
    corps_accessibles_fusee_1 = corps_celestes_accessibles(fusees[0])  # TODO Remplacer list() par le bon appel de fonction
    corps_accessibles_fusee_2 = corps_celestes_accessibles(fusees[1])  # TODO Remplacer list() par le bon appel de fonction
    print(f"Fusée 1 ({fusees[0].nom}) peut aller jusqu'à {','.join(corps_accessibles_fusee_1)}")
    print(f"Fusée 2 ({fusees[1].nom}) peut aller jusqu'à {','.join(corps_accessibles_fusee_2)}")

    # TODO Créez et affichez le graphique de comparaison des deux fusées en réutilisant la fonction implémentée
    print(comparer_fusee(fusees[0], fusees[1]))
    return fusees[0], fusees[1]


if __name__ == '__main__':
    main()
