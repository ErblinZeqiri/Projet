# data_gestion_films.py
# EZ 2020.04.27 Permet de gérer (CRUD) les données de la table t_films


from flask import flash

from APP_FILMS.DATABASE import connect_db_context_manager
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
            flash("Dans Gestion films ...terrible erreur, il faut connecter une base de donnée", "Danger")
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Exception grave Classe constructeur GestionFilms {erreur.args[0]}")
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



    # def add_films(self, nom_films, duree_films, date_sortie_films):
    def add_films(self, valeurs_insertion_dictionnaire):
        try:
            # # Définitions d'un dictionnaire pour passer les valeurs en paramètres de façon un "peu" sécurisée dans la BD
            # valeurs_insertion_dictionnaire = {'value_nom_films': valeur_ins_1, 'value_duree_films': valeur_ins_2,
            #                                   'date_sortie_films': valeur_ins_3}
            # Rssure la personne qui dévelloppe que les valeurs à insérer sont bien à disposition.
            print(valeurs_insertion_dictionnaire)
            str_sql_insert = "INSERT INTO t_serveur (ID_Serveur, Nom_Serv, Nombre_Port, Nombre_U, Date_Conf_Serv, " \
                             ", Puissance, Date_Serveur) " \
                             "VALUES (NULL, %(value_Nom_Serv)s, %(value_Nombre_Port)s, %(value_Nombre_U)s, " \
                             "%(value_Date_Conf_Serv)s, %(value_Description)s), " \
                             "%(value_Puissance)s), %(value_Date_Serveur)s))"
            with MaBaseDeDonnee() as ma_bd_curseur:
                # OM Méthode "execute" définie simplement pour raccourcir la ligne de code
                # ligne de code normale : ma_bd_moi.connexion_bd.cursor(str_sql_insert, valeurs_insertion_dictionnaire)
                ma_bd_curseur.execute(str_sql_insert, valeurs_insertion_dictionnaire)

        except Exception as erreur:
            # OM 2020.04.09 DIFFERENTS MOYENS D'INFORMER EN CAS D'ERREURS.
            # Message dans la console en cas d'échec du bon déroulement des commandes ci-dessus.
            print("Data Gestions Films ERREUR: {0}".format(erreur))
            print(f"Print console ... Data Gestions Films, numéro de l'erreur : {erreur}")
            # Petits messages "flash", échange entre Python et Jinja dans une page en HTML
            flash(f"Flash ... Data Gestions Films, numéro de l'erreur : {erreur}")
            # raise, permet de "lever" une exception et de personnaliser la page d'erreur
            # voir fichier "run_mon_app.py"

            print("erreur args.. ",erreur.args)
            code, msg = erreur.args
            print(" codes d'erreurs ---> ", error_codes.get(code, msg))
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise Exception(f"Raise exception... Data Gestions Films {erreur}")

    def edit_film_data(self, valeur_id_dictionnaire):
            try:
                print(valeur_id_dictionnaire)
                # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                # Commande MySql pour afficher le films sélectionné dans le tableau dans le formulaire HTML
                str_sql_id_films = "SELECT ID_Serveur, Nom_Serv FROM t_serveur WHERE ID_Serveur = %(value_id_films)s"

                # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
                # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
                # sera interprété, ainsi on fera automatiquement un commit
                with MaBaseDeDonnee().connexion_bd as mconn_bd:
                    with mconn_bd as mc_cur:
                        mc_cur.execute(str_sql_id_films, valeur_id_dictionnaire)
                        data_one = mc_cur.fetchall()
                        print("valeur_id_dictionnaire...", data_one)
                        return data_one

            except Exception as erreur:
                # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème edit_films_data Data Gestions films numéro de l'erreur : {erreur}")
                # flash(f"Flash. Problèmes Data Gestions films numéro de l'erreur : {erreur}", "danger")
                # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
                # Ainsi on peut avoir un message d'erreur personnalisé.
                raise Exception(
                    "Raise exception... Problème edit_films_data d'un films Data Gestions films {erreur}")

    def update_films_data(self, valeur_update_dictionnaire):
            try:
                print(valeur_update_dictionnaire)
                # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulefilmHTML" du form HTML "filmEdit.html"
                # le "%s" permet d'éviter des injections SQL "simples"
                # <td><input type = "text" name = "nameEditIntitulefilmsHTML" value="{{ row.intitule_films }}"/></td>
                str_sql_update_intitulefilms = "UPDATE t_personne SET Nom_Pers = %(value_name_films)s WHERE ID_Personne = %(value_id_films)s"

                # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
                # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
                # sera interprété, ainsi on fera automatiquement un commit
                with MaBaseDeDonnee().connexion_bd as mconn_bd:
                    with mconn_bd as mc_cur:
                        mc_cur.execute(str_sql_update_intitulefilms, valeur_update_dictionnaire)

            except (Exception,
                    pymysql.err.OperationalError,
                    pymysql.ProgrammingError,
                    pymysql.InternalError,
                    pymysql.IntegrityError,
                    TypeError) as erreur:
                # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
                print(f"Problème update_films_data Data Gestions films numéro de l'erreur : {erreur}")
                # flash(f"Flash. Problèmes Data Gestions films numéro de l'erreur : {erreur}", "danger")
                # raise Exception('Raise exception... Problème update_films_data d\'un films Data Gestions films {}'.format(str(erreur)))
                if erreur.args[0] == 1062:
                    flash(f"Flash. Cette valeur existe déjà : {erreur}", "danger")
                    # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                    flash('Doublon !!! Introduire une valeur différente')
                    # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                    print(f"Problème update_films_data Data Gestions films numéro de l'erreur : {erreur}")

                    raise Exception(
                        "Raise exception... Problème update_films_data d'un films DataGestionsfilms {erreur}")