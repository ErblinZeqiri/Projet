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
            print(f"Exception grave Classe constructeur Gestionfilms {erreur.args[0]}")
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

    def add_film_data(self, valeurs_insertion_dictionnaire):
            try:
                print(valeurs_insertion_dictionnaire)
                # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                strsql_insert_film = """INSERT INTO `t_serveur` (`ID_Serveur`, `Nom_Serv`, `Nombre_Port`, `Nombre_U`,
                                    `Date_Conf_Serv`, `Description`, `Puissance`) VALUES (NULL, %(value_Nom_Serv)s,
                                    %(value_Nombre_Port)s, %(value_Nombre_U)s, %(value_Date_Conf_Serv)s, %(value_Description)s,
                                    %(value_Puissance)s)"""

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

    def edit_film_data(self, valeur_id_dictionnaire):
                try:
                    print(valeur_id_dictionnaire)
                    # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # Commande MySql pour afficher le film sélectionné dans le tableau dans le formulaire HTML
                    str_sql_id_film = """SELECT ID_Serveur, Nom_Serv , Nombre_Port, Nombre_U, Date_Conf_Serv,
                                        Description, Puissance FROM t_serveur WHERE ID_Serveur = %(value_ID_Serveur)s"""

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
                    # sera interprété, ainsi on fera automatiquement un commit
                    with MaBaseDeDonnee().connexion_bd as mconn_bd:
                        with mconn_bd as mc_cur:
                            mc_cur.execute(str_sql_id_film, valeur_id_dictionnaire)
                            data_one = mc_cur.fetchall()
                            print("valeur_id_dictionnaire...", data_one)
                            return data_one

                except Exception as erreur:
                    # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
                    print(f"Problème edit_film_data Data Gestions films numéro de l'erreur : {erreur}")
                    # flash(f"Flash. Problèmes Data Gestions films numéro de l'erreur : {erreur}", "danger")
                    # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
                    # Ainsi on peut avoir un message d'erreur personnalisé.
                    raise Exception(
                        "Raise exception... Problème edit_film_data d'un film Data Gestions films {erreur}")

    def update_film_data(self, valeur_update_dictionnaire):
                try:
                    print(valeur_update_dictionnaire)
                    # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulefilmHTML" du form HTML "filmsEdit.html"
                    # le "%s" permet d'éviter des injections SQL "simples"
                    # <td><input type = "text" name = "nameEditIntitulefilmHTML" value="{{ row.intitule_film }}"/></td>
                    str_sql_update_intitulefilm = "UPDATE t_serveur SET Nom_Serv = %(value_Nom_Serv)s, Nombre_Port = %(value_Nombre_Port)s," \
                                                  " Nombre_U = %(value_Nombre_U)s, Date_Conf_Serv = %(value_Date_Conf_Serv)s," \
                                                  " Description = %(value_Description)s, Puissance = %(value_Puissance)s " \
                                                  "WHERE ID_Serveur = %(value_ID_Serveur)s"

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
                    # sera interprété, ainsi on fera automatiquement un commit
                    with MaBaseDeDonnee().connexion_bd as mconn_bd:
                        with mconn_bd as mc_cur:
                            mc_cur.execute(str_sql_update_intitulefilm, valeur_update_dictionnaire)

                except (Exception,
                        pymysql.err.OperationalError,
                        pymysql.ProgrammingError,
                        pymysql.InternalError,
                        pymysql.IntegrityError,
                        TypeError) as erreur:
                    # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
                    print(f"Problème update_film_data Data Gestions films numéro de l'erreur : {erreur}")
                    # flash(f"Flash. Problèmes Data Gestions films numéro de l'erreur : {erreur}", "danger")
                    # raise Exception('Raise exception... Problème update_film_data d\'un film Data Gestions films {}'.format(str(erreur)))
                    if erreur.args[0] == 1062:
                        flash(f"Flash. Cette valeur existe déjà : {erreur}", "danger")
                        # Deux façons de communiquer une erreur causée par l'insertion d'une valeur à double.
                        flash(f"'Doublon !!! Introduire une valeur différente", "warning")
                        # Message en cas d'échec du bon déroulement des commandes ci-dessus.
                        print(f"Problème update_film_data Data Gestions films numéro de l'erreur : {erreur}")

                        raise Exception(
                            "Raise exception... Problème update_film_data d'un film DataGestionsfilms {erreur}")

    def delete_select_film_data(self, valeur_delete_dictionnaire):
                        try:
                            print(valeur_delete_dictionnaire)
                            # OM 2019.04.02 Commande MySql pour la MODIFICATION de la valeur "CLAVIOTTEE" dans le champ "nameEditIntitulefilmHTML" du form HTML "filmsEdit.html"
                            # le "%s" permet d'éviter des injections SQL "simples"
                            # <td><input type = "text" name = "nameEditIntitulefilmHTML" value="{{ row.intitule_film }}"/></td>

                            # OM 2020.04.07 C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                            # Commande MySql pour afficher le film sélectionné dans le tableau dans le formulaire HTML
                            str_sql_select_ID_Serveur = """SELECT ID_Serveur, Nom_Serv , Nombre_Port, Nombre_U, Date_Conf_Serv,
                                                        Description, Puissance, Date_Serveur FROM t_serveur WHERE ID_Serveur = %(value_ID_Serveur)s"""

                            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
                            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
                            # sera interprété, ainsi on fera automatiquement un commit
                            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                                with mconn_bd as mc_cur:
                                    mc_cur.execute(str_sql_select_ID_Serveur, valeur_delete_dictionnaire)
                                    data_one = mc_cur.fetchall()
                                    print("valeur_id_dictionnaire...", data_one)
                                    return data_one

                        except (Exception,
                                pymysql.err.OperationalError,
                                pymysql.ProgrammingError,
                                pymysql.InternalError,
                                pymysql.IntegrityError,
                                TypeError) as erreur:
                            # DEBUG bon marché : Pour afficher un message dans la console.
                            print(f"Problème delete_select_film_data Gestions films numéro de l'erreur : {erreur}")
                            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                            flash(f"Flash. Problème delete_select_film_data numéro de l'erreur : {erreur}", "danger")
                            raise Exception(
                                "Raise exception... Problème delete_select_film_data d\'un film Data Gestions films {erreur}")

    def delete_film_data(self, valeur_delete_dictionnaire):
                        try:
                            print(valeur_delete_dictionnaire)
                            # OM 2019.04.02 Commande MySql pour EFFACER la valeur sélectionnée par le "bouton" du form HTML "filmsEdit.html"
                            # le "%s" permet d'éviter des injections SQL "simples"
                            # <td><input type = "text" name = "nameEditIntitulefilmHTML" value="{{ row.intitule_film }}"/></td>
                            str_sql_delete_intitulefilm = "DELETE FROM t_serveur WHERE ID_Serveur = %(value_ID_Serveur)s"

                            # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                            # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
                            # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
                            # sera interprété, ainsi on fera automatiquement un commit
                            with MaBaseDeDonnee().connexion_bd as mconn_bd:
                                with mconn_bd as mc_cur:
                                    mc_cur.execute(str_sql_delete_intitulefilm, valeur_delete_dictionnaire)
                                    data_one = mc_cur.fetchall()
                                    print("valeur_id_dictionnaire...", data_one)
                                    return data_one
                        except (Exception,
                                pymysql.err.OperationalError,
                                pymysql.ProgrammingError,
                                pymysql.InternalError,
                                pymysql.IntegrityError,
                                TypeError) as erreur:
                            # DEBUG bon marché : Pour afficher un message dans la console.
                            print(f"Problème delete_film_data Data Gestions films numéro de l'erreur : {erreur}")
                            # flash(f"Flash. Problèmes Data Gestions films numéro de l'erreur : {erreur}", "danger")
                            if erreur.args[0] == 1451:
                                # OM 2020.04.09 Traitement spécifique de l'erreur 1451 Cannot delete or update a parent row: a foreign key constraint fails
                                # en MySql le moteur INNODB empêche d'effacer un film qui est associé à un film dans la table intermédiaire "t_films_films"
                                # il y a une contrainte sur les FK de la table intermédiaire "t_films_films"
                                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                                # flash(f"Flash. IMPOSSIBLE d'effacer !!! Ce film est associé à des films dans la t_films_films !!! : {erreur}", "danger")
                                # DEBUG bon marché : Pour afficher un message dans la console.
                                print(
                                    f"IMPOSSIBLE d'effacer !!! Ce film est associé à des films dans la t_films_films !!! : {erreur}")
                            raise MaBdErreurDelete(
                                f"DGG Exception {msg_erreurs['ErreurDeleteContrainte']['message']} {erreur}")
