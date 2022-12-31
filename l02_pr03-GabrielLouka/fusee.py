import math

from numpy import degrees

from constantes import MASSE_VOLUMIQUE_CARBURANT, CHAMP_GRAVITATIONNEL


class Piece:
    def __init__(self, nom: str, hauteur: float, masse: float, prix: float) -> None:
        self.nom = nom
        self.hauteur = hauteur  # En m
        self.masse = masse  # En kg
        self.prix = prix  # En $CAN

    def __str__(self) -> str:
        return f"{self.nom}, hauteur={self.hauteur}m, masse={self.masse}kg, prix={self.prix}$"


class Capsule(Piece):
    def __init__(self, nom: str, hauteur: float, masse: float, prix: float, places: int) -> None:
        super().__init__(nom, hauteur, masse, prix)

        self.places = places  # En personnes

    def __str__(self) -> str:
        return f"Capsule: {super().__str__()}, places={self.places} personne(s)"


class Reservoir(Piece):
    def __init__(self, nom: str, hauteur: float, masse_vide: float, prix: float, capacite: float) -> None:
        super().__init__(nom, hauteur, masse_vide, prix)
 
        self.capacite = capacite  # En litres

    def __str__(self) -> str:
        return f"Réservoir: {super().__str__()}, capacité={self.capacite}L"

    @property
    def masse_rempli(self) -> float:
        # TODO calculez la masse du réservoir rempli.
        #  Utilisez MASSE_VOLUMIQUE_CARBURANT
        return (MASSE_VOLUMIQUE_CARBURANT * self.capacite) + self.masse


class Moteur(Piece):
    def __init__(self, nom: str, hauteur: float, masse: float, prix: float, impulsion_specifique: int) -> None:
        super().__init__(nom, hauteur, masse, prix)

        self.impulsion_specifique = impulsion_specifique  # En secondes

    def __str__(self) -> str:
        return f"Moteur: {super().__str__()}, impulsion spécifique={self.impulsion_specifique}s"


class Fusee:
    """
    La classe représentant une fusée simple.

    Une fusée a comme attributs publics:
    * Un nom

    Une fusée a comme attributs privés:
    * Une capsule
    * Un réservoir
    * Un moteur
    """

    # TODO Implanter le constructeur avec les différentes pièces comme attributs privés
    def __init__(self, nom, capsule, reservoir, moteur) -> None:
        self.nom = nom
        self.__capsule = capsule
        self.__reservoir = reservoir
        self.__moteur = moteur

    def __str__(self) -> str:
        # TODO Implantez la fonction __str__ pour permettre l'affichage de la fusée
        description = (
        'Fusée:\n'
        f'\tNom: {self.nom}\n'
        f'\tHauteur totale: {self.hauteur}m\n'
        f'\tMasse totale (remplie): {self.masse}kg\n'
        f'\tPrix total: {self.prix}$\n'
        'Pièces:\n'
        f'\tCapsule: {self.__capsule.nom}, hauteur={self.__capsule.hauteur}m, masse={self.__capsule.masse}kg, prix={self.__capsule.prix}$, places={self.__capsule.places} personne(s)\n'
        f'\tRéservoir: {self.__reservoir.nom}, hauteur={self.__reservoir.hauteur}m, masse={self.__reservoir.masse}kg, prix={self.__reservoir.prix}$, capacité={self.__reservoir.capacite}L\n'
        f'\tMoteur: {self.__moteur.nom}, hauteur={self.__moteur.hauteur}m, masse={self.__moteur.masse}kg, prix={self.__moteur.prix}$, impulsion spécifique={self.__moteur.impulsion_specifique}s'
        )
        
        return description

    @property
    def masse(self) -> float:
        # TODO Calculez la masse totale de la fusée (incluant le carburant)
        print('capsule',  self.__capsule)
        print('nom',  self.nom)
        print('reservoir',  self.__reservoir)
        print('moteur',  self.__moteur)
        return self.__capsule.masse + self.__reservoir.masse_rempli + self.__moteur.masse
    
    @property
    def hauteur(self) -> float:
        # TODO Calculez la hauteur totale de la fusée
        return self.__capsule.hauteur + self.__moteur.hauteur + self.__reservoir.hauteur

    @property
    def prix(self) -> float:
        # TODO Calculez le prix total de la fusée
        return self.__capsule.prix + self.__moteur.prix + self.__reservoir.prix

    def calculer_deltav(self) -> float:
        # TODO À partir de la masse, du moteur et du réservoir,
        #  calculez le deltaV disponible de la fusée dans l'atmosphère
        #  Utilisez la constante CHAMP_GRAVITATIONNEL
        masse_tot = self.__capsule.masse + self.__reservoir.masse_rempli + self.__moteur.masse 
        masse_sans_carb = self.__capsule.masse + self.__reservoir.masse + self.__moteur.masse 
        return self.__moteur.impulsion_specifique * CHAMP_GRAVITATIONNEL * math.log((masse_tot/masse_sans_carb))


if __name__ == '__main__':
    # Reservoir.masse_rempli
    reservoir = Reservoir("Pichet", 0.4, 0.5, 20, 2)
    masse_rempli = reservoir.masse_rempli
    print(f"Une fois rempli, {reservoir.nom} a une masse de {masse_rempli} kg")
    print()

    # Fusee constructeur
    capsule = Capsule("Exigüe", 1.0, 750, 1300.0, 1)
    reservoir = Reservoir("Pichet", 0.4, 0.5, 20.0, 2)
    moteur = Moteur("Pantera Arctic Cat Triple 800", 4, 2000, 14000.0, 199)
    fusee = Fusee("Romano Fafard", capsule, reservoir, moteur)

    # Fusee.masse
    print(f"La masse de la fusée {fusee.nom} est {fusee.masse}kg")
    print()

    # Fusee.hauteur
    print(f"La hauteur de la fusée {fusee.nom} est {fusee.hauteur}m")
    print()

    # Fusee.prix
    print(f"Le prix de la fusée {fusee.nom} est {fusee.prix}$")
    print()

    # Fusee.__str__
    print(f"fusee est de type {type(fusee)}")
    print()
