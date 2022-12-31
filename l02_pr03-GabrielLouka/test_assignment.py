import json
import os
import sys
import tempfile
import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pandas as pd
from matplotlib import pyplot as plt
from pandas._testing import assert_frame_equal

from assemblage import creer_capsules, creer_moteurs, creer_reservoirs, corps_celestes_accessibles, comparer_fusee
from constantes import FICHIER_CAPSULE, FICHIERS_RESERVOIRS, FICHIERS_MOTEURS
from fichiers_pieces import filtrer_moteurs, charger_capsules_df, charger_reservoirs_df, charger_moteurs_df
from fusee import Fusee, Capsule, Reservoir, Moteur
from main import main

TEST_CAPSULES = [{'nom': 'nom1', 'hauteur': 1.1, 'masse': 1.1, 'prix': 1.1, 'places': 1},
                 {'nom': 'nom2', 'hauteur': 2.2, 'masse': 2.2, 'prix': 2.2, 'places': 2},
                 {'nom': 'nom3', 'hauteur': 3.3, 'masse': 3.3, 'prix': 3.3, 'places': 3}]

TEST_RESERVOIRS = [{'nom': 'nom1', 'hauteur': 1.1, 'masse': 1.1, 'prix': 1.1, 'capacite': 1},
                   {'nom': 'nom2', 'hauteur': 2.2, 'masse': 2.2, 'prix': 2.2, 'capacite': 2},
                   {'nom': 'nom3', 'hauteur': 3.3, 'masse': 3.3, 'prix': 3.3, 'capacite': 3}]

TEST_MOTEURS = [{'nom': 'nom1', 'hauteur': 1.1, 'masse': 1.1, 'prix': 1.1, 'impulsion specifique': 1},
                {'nom': 'nom2', 'hauteur': 2.2, 'masse': 2.2, 'prix': 2.2, 'impulsion specifique': 2},
                {'nom': 'nom3', 'hauteur': 3.3, 'masse': 3.3, 'prix': 3.3, 'impulsion specifique': 3},
                {'nom': 'nom4', 'hauteur': 4.4, 'masse': 4.4, 'prix': 4.4, 'impulsion specifique': 4}]

TEST_MOTEURS_MAIN = [{'nom': 'moteur10', 'hauteur': 10.10, 'masse': 10.10, 'prix': 10.10, 'impulsion specifique': 300},
                     {'nom': 'moteur20', 'hauteur': 20.20, 'masse': 20.20, 'prix': 20.20, 'impulsion specifique': 300}]


class TestFichiersPieces(TestCase):
    def test_charger_capsules_df(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with open(f"{tmp_dir}/{FICHIER_CAPSULE}", "w") as f:
                f.write("n,h,m,p,pl\nnom1,1.1,1.1,1.1,1\nnom2,2.2,2.2,2.2,2\nnom3,3.3,3.3,3.3,3")

            df = charger_capsules_df(tmp_dir)
            assert_frame_equal(df, pd.DataFrame(TEST_CAPSULES))

    def test_charger_reservoirs_df(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            for i, reservoir in enumerate(TEST_RESERVOIRS):
                with open(f"{tmp_dir}/{FICHIERS_RESERVOIRS[i]}", "w") as f:
                    f.write(json.dumps([reservoir]))

            df = charger_reservoirs_df(tmp_dir)
            assert_frame_equal(df, pd.DataFrame(TEST_RESERVOIRS))

    def test_charger_moteurs_df_1(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            for i, moteur in enumerate(TEST_MOTEURS):
                with open(f"{tmp_dir}/{FICHIERS_MOTEURS[i]}", "w") as f:
                    f.write(f"#comment\n"
                            f"nom={moteur['nom']}\n"
                            f"hauteur={moteur['hauteur']}\n"
                            f"masse={moteur['masse']}\n"
                            "\n"
                            f"prix={moteur['prix']}\n"
                            f"impulsion specifique={moteur['impulsion specifique']}\n")

            df = charger_moteurs_df(tmp_dir)
            assert_frame_equal(df, pd.DataFrame(TEST_MOTEURS))

    def test_charger_moteurs_df_2(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            for i, moteur in enumerate(TEST_MOTEURS):
                with open(f"{tmp_dir}/{FICHIERS_MOTEURS[i]}", "w") as f:
                    f.write(f"# Moteur conçu par le Poly Propulsion Lab (PPL)\n"
                            f"nom={moteur['nom']}\n"
                            "\n"
                            "# Propriétés générales\n"
                            f"hauteur={moteur['hauteur']:.1f}\n"
                            f"masse={moteur['masse']:.1f}\n"
                            f"prix={moteur['prix']:.2f}\n"
                            "\n"
                            f"impulsion specifique={moteur['impulsion specifique']}\n")

            df = charger_moteurs_df(tmp_dir)
            assert_frame_equal(df, pd.DataFrame(TEST_MOTEURS))

    def test_filtrer_moteurs(self):
        test_df = pd.DataFrame(TEST_MOTEURS.copy())

        expected_df = test_df.copy().drop(0)

        assert_frame_equal(filtrer_moteurs(test_df, 1), expected_df,
                           "Le dataframe de moteur n'a pas été filtré correctement")

    def test_filtrer_moteurs_vide(self):
        test_moteurs = [{'nom': 'nom1', 'hauteur': 1.0, 'masse': 1.0, 'prix': 1.0, 'impulsion specifique': 1}]
        test_df = pd.DataFrame(test_moteurs)

        expected_df = test_df.copy()[0:0]

        assert_frame_equal(filtrer_moteurs(test_df, sys.maxsize), expected_df, "Le dataframe filtré devrait être vide")


class TestFuseeConstructeur(TestCase):
    def test_fusee_constructeur_existe(self):
        try:
            capsule = Capsule("Exigüe", 1.0, 750, 1300.0, 1)
            reservoir = Reservoir("Pichet", 0.4, 0.5, 20.0, 2)
            moteur = Moteur("Pantera Arctic Cat Triple 800", 4, 2000, 14000.0, 199)
            Fusee("Romano Fafard", capsule, reservoir, moteur)
        except AttributeError:
            self.fail("Le constructeur de Fusee n'a pas été implanté correctement")


class TestFusee(TestCase):
    def setUp(self) -> None:
        capsule = Capsule("Exigüe", 1.0, 750, 1300.0, 1)
        reservoir = Reservoir("Pichet", 0.4, 0.5, 20.0, 2)
        moteur = Moteur("Pantera Arctic Cat Triple 800", 4, 2000, 14000.0, 199)
        self.fusee = Fusee("Romano Fafard", capsule, reservoir, moteur)

    def test_fusee_attribut_nom(self):
        try:
            self.fusee.nom
        except AttributeError:
            self.fail("La fusée devrait avoir un attribut public nommé nom")

    def test_fusee_attribut_capsule(self):
        try:
            # Syntaxe de test, ne pas utiliser dans la vraie vie!
            self.fusee._Fusee__capsule
        except AttributeError:
            self.fail("La fusée devrait avoir un attribut privé nommé capsule")

    def test_fusee_attribut_reservoir(self):
        try:
            # Syntaxe de test, ne pas utiliser dans la vraie vie!
            self.fusee._Fusee__reservoir
        except AttributeError:
            self.fail("La fusée devrait avoir un attribut privé nommé reservoir")

    def test_fusee_attribut_moteur(self):
        try:
            # Syntaxe de test, ne pas utiliser dans la vraie vie!
            self.fusee._Fusee__moteur
        except AttributeError:
            self.fail("La fusée devrait avoir un attribut privé nommé moteur")

    def test_reservoir_masse_rempli(self):
        reservoir = Reservoir("Pichet", 0.4, 0.5, 20.0, 2)
        self.assertAlmostEqual(reservoir.masse_rempli, 100.5,
                               msg="La masse d'un pichet de carburant devrait être 100.5 litres")

    def test_fusee_str(self):
        expected = (
            'Fusée:\n'
            '\tNom: Romano Fafard\n'
            '\tHauteur totale: 5.4m\n'
            '\tMasse totale (remplie): 2850.5kg\n'
            '\tPrix total: 15320.0$\n'
            'Pièces:\n'
            '\tCapsule: Exigüe, hauteur=1.0m, masse=750kg, prix=1300.0$, places=1 personne(s)\n'
            '\tRéservoir: Pichet, hauteur=0.4m, masse=0.5kg, prix=20.0$, capacité=2L\n'
            '\tMoteur: Pantera Arctic Cat Triple 800, hauteur=4m, masse=2000kg, prix=14000.0$, impulsion spécifique=199s'
        )

        print(self.fusee)
        self.assertEqual(str(self.fusee), expected, "La représentation en str de Fusee n'est pas comme attendue.")

    def test_fusee_masse(self):
        self.assertAlmostEqual(self.fusee.masse, 2850.5,
                               msg="La masse totale de la fusée remplie de carburant n'est pas celle attendue.")

    def test_fusee_hauteur(self):
        self.assertAlmostEqual(self.fusee.hauteur, 5.4,
                               msg="La hauteur totale de la fusée n'est pas celle attendue.")

    def test_fusee_prix(self):
        self.assertAlmostEqual(self.fusee.masse, 2850.5,
                               msg="Le prix total de la fusée n'est pas celui attendu.")

    def test_fusee_deltaV(self):
        self.assertAlmostEqual(self.fusee.calculer_deltav(), 69.71603173654347,
                               msg="Le deltaV de la fusée n'est pas celui attendu.")


class TestAssemblage(TestCase):
    def test_creer_capsules(self):
        test_df = pd.DataFrame(TEST_CAPSULES)

        capsules = creer_capsules(test_df)
        self.assertIsInstance(capsules, list, "creer_capsules doit retourner une liste")
        self.assertEqual(len(capsules), len(TEST_CAPSULES),
                         "La liste de capsules doit être de la même taille que le dataframe")
        self.assertIsInstance(capsules[0], Capsule, "Les objets de la liste doivent être des Capsule")

        for i in range(len(TEST_CAPSULES)):
            capsule = capsules[i]
            self.assertEqual(capsule.nom, f"nom{i + 1}")
            self.assertAlmostEqual(capsule.hauteur, float((i + 1) * 1.1))
            self.assertAlmostEqual(capsule.masse, float((i + 1) * 1.1))
            self.assertAlmostEqual(capsule.prix, float((i + 1) * 1.1))
            self.assertAlmostEqual(capsule.places, i + 1)

    def test_creer_moteurs(self):
        test_df = pd.DataFrame(TEST_MOTEURS)

        moteurs = creer_moteurs(test_df)
        self.assertIsInstance(moteurs, list, "creer_moteurs doit retourner une liste")
        self.assertEqual(len(moteurs), len(TEST_MOTEURS),
                         "La liste de moteurs doit être de la même taille que le dataframe")
        self.assertIsInstance(moteurs[0], Moteur, "Les objets de la liste doivent être des Moteur")

        for i in range(len(TEST_MOTEURS)):
            moteur = moteurs[i]
            self.assertEqual(moteur.nom, f"nom{i + 1}")
            self.assertAlmostEqual(moteur.hauteur, float((i + 1) * 1.1))
            self.assertAlmostEqual(moteur.masse, float((i + 1) * 1.1))
            self.assertAlmostEqual(moteur.prix, float((i + 1) * 1.1))
            self.assertAlmostEqual(moteur.impulsion_specifique, i + 1)

    def test_creer_reservoirs(self):
        test_df = pd.DataFrame(TEST_RESERVOIRS)

        reservoirs = creer_reservoirs(test_df)
        self.assertIsInstance(reservoirs, list, "creer_reservoirs doit retourner une liste")
        self.assertEqual(len(reservoirs), len(TEST_RESERVOIRS),
                         "La liste de reservoirs doit être de la même taille que le dataframe")
        self.assertIsInstance(reservoirs[0], Reservoir, "Les objets de la liste doivent être des Reservoir")

        for i in range(len(TEST_RESERVOIRS)):
            reservoir = reservoirs[i]
            self.assertEqual(reservoir.nom, f"nom{i + 1}")
            self.assertAlmostEqual(reservoir.hauteur, float((i + 1) * 1.1))
            self.assertAlmostEqual(reservoir.masse, float((i + 1) * 1.1))
            self.assertAlmostEqual(reservoir.prix, float((i + 1) * 1.1))
            self.assertAlmostEqual(reservoir.capacite, i + 1)

    def test_corps_celestes_accessibles(self):
        capsule = Capsule("Exigüe", 1.0, 750, 1300.0, 1)
        reservoir = Reservoir("Gros Pichet", 0.4, 0.5, 20.0, 600)
        moteur = Moteur("Pantera Arctic Cat Triple 800", 4, 2000, 14000.0, 199)
        fusee = Fusee("Romano Fafard+", capsule, reservoir, moteur)

        corps_accessibles = corps_celestes_accessibles(fusee)
        corps_attendus = ['Vénus', 'Mars']
        self.assertEqual(corps_accessibles, corps_attendus)

    def test_comparer_fusee(self):
        capsule = Capsule("Exigüe", 1.0, 750, 1300.0, 1)
        reservoir_1 = Reservoir("Gros Pichet", 0.4, 0.5, 20.0, 600)
        reservoir_2 = Reservoir("Gros Pichet", 0.4, 0.5, 20.0, 2)
        moteur = Moteur("Pantera Arctic Cat Triple 800", 4, 2000, 14000.0, 199)
        fusee_1 = Fusee("Romano Fafard+", capsule, reservoir_1, moteur)
        fusee_2 = Fusee("Romano Fafard", capsule, reservoir_2, moteur)

        # Disable show
        plt.show = MagicMock()

        comparer_fusee(fusee_1, fusee_2)
        # Assert plt.show() was called
        plt.show.assert_called()

 
class TestMain(TestCase):

    @patch('builtins.input', side_effect=["fusee1", 0, 0, 0, "fusee2", 1, 1, 1])
    @patch('main.charger_capsules_df', return_value=pd.DataFrame(TEST_CAPSULES))
    @patch('main.charger_reservoirs_df', return_value=pd.DataFrame(TEST_RESERVOIRS))
    @patch('main.charger_moteurs_df', return_value=pd.DataFrame(TEST_MOTEURS_MAIN))
    def test_main(self, mock_inputs, mock_charger_capsules_df, mock_charger_reservoirs_df, mock_charger_moteurs_df):
        # Disable show
        plt.show = MagicMock()

        fusees = main()
        self.assertIsInstance(fusees[0], Fusee)
        self.assertIsInstance(fusees[1], Fusee)


if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.mkdir('logs')
    with open('logs/tests_results.txt', 'w') as f:
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(sys.modules[__name__])
        unittest.TextTestRunner(f, verbosity=2).run(suite)
