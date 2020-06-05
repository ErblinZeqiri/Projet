# data_gestion_films.py
# OM 2698.03.21 Permet de gérer (CRUD) les données de la table t_films


from flask import render_template, flash, request, redirect, url_for
from APP_FILMS import obj_mon_application
from APP_FILMS.DATABASE.connect_db_context_manager import MaBaseDeDonnee
from APP_FILMS.DATABASE.erreurs import *



class GestionFilms():
    def __init__(self):
        try:
            print("dans le try de gestions films")
            # OM 2020.04.11 La connexion à la base de données est-elle active ?
            # Renvoie une erreur si la connexion est perdue.
            MaBaseDeDonnee().connexion_bd.ping(False)
        except Exception as erreur:
            flash("Dans Gestion films ...terrible erreur, il faut connecter une base de donnée", "danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionGenres {erreur.args[0]}")
            raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

        print("Classe constructeur GestionFilms ")


    def films_afficher_data(self):
        try:
            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
            # la commande MySql classique est "SELECT * FROM t_films"
            # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
            # donc, je précise les champs à afficher
            strsql_films_afficher = """SELECT ID_Serveur, Nom_Serv, Nombre_Port, Nombre_U,
                                        Date_Conf_Serv, Description, Puissance, Date_Serveur FROM t_serveur"""
            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                # Envoi de la commande MySql
                mc_afficher.execute(strsql_films_afficher)
                # Récupère les données de la requête.
                data_films = mc_afficher.fetchall()
                # Affichage dans la console
                print("data_films ", data_films, " Type : ", type(data_films))
                # Retourne les données du "SELECT"
                return data_films
        except pymysql.Error as erreur:
            print(f"DGF gad pymysql errror {erreur.args[0]} {erreur.args[1]}")
            raise  MaBdErreurPyMySl(f"DGG fad pymysql errror {msg_erreurs['ErreurPyMySql']['message']} {erreur.args[0]} {erreur.args[1]}")
        except Exception as erreur:
            print(f"DGF gad Exception {erreur.args}")
            raise MaBdErreurConnexion(f"DGG fad Exception {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args}")
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # raise MaBdErreurDoublon(f"{msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")
            raise MaBdErreurConnexion(f"DGF fad pei {msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[1]}")

    def add_films_data(self, valeurs_insertion_dictionnaire):
            try:
                print(valeurs_insertion_dictionnaire)
                # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                #strsql_insert_film = """INSERT INTO `t_serveur` (`ID_Serveur`, `Nom_Serv`, `Nombre_Port`, `Nombre_U`,
                #                    `Date_Conf_Serv`, `Description`, `Puissance`, `Date_Serveur`) VALUES (NULL, %(value_Nom_Serv)s,
                 #                   %(value_Nombre_Port)s, %(value_Nombre_U)s, %(value_Date_Conf_Serv)s, %(value_Description)s,
                  #                  %(value_Puissance)s)"""

                strsql_insert_film = """INSERT INTO `t_serveur`(`ID_Serveur`, `Nom_Serv`, `Nombre_Port`, `Nombre_U`, 
                                        `Date_Conf_Serv`, `Description`, `Puissance`, `Date_Serveur`)
                                        VALUES(NULL, 'asd', '234', '2111', '2020-03-25', 'ewrwreew', 
                                        '21321321', CURRENT_TIMESTAMP);"""
                # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
                # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
                # sera interprété, ainsi on fera automatiquement un commit
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_film, valeurs_insertion_dictionnaire)


            except pymysql.err.IntegrityError as erreur:
                # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
                # Ainsi on peut avoir un message d'erreur personnalisé.
                raise MaBdErreurDoublon(
                    f"DGG pei erreur doublon {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")