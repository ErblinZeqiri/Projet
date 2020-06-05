# routes_gestion_films.py
# OM 2020.04.06 Gestions des "routes" FLASK pour les films.
import re

import pymysql
from flask import render_template, flash, request, url_for
from werkzeug.utils import redirect
from APP_FILMS.DATABASE.erreurs import *

from APP_FILMS import obj_mon_application
from APP_FILMS.FILMS.data_gestion_films import GestionFilms, MaBdErreurConnexion


# OM 2020.04.16 Afficher un avertissement sympa...mais contraignant
# Pour la tester http://127.0.0.1:5005/avertissement_sympa_pour_geeks
@obj_mon_application.route("/avertissement_sympa_pour_geeks")
def avertissement_sympa_pour_geeks():
    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("films/AVERTISSEMENT_SYMPA_POUR_LES_GEEKS_films.html")




# OM 2020.04.16 Afficher les films
# Pour la tester http://127.0.0.1:5005/films_afficher
@obj_mon_application.route("/films_afficher")
def films_afficher():
    # OM 2020.04.09 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_films = GestionFilms()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionFilms()
            # Fichier data_gestion_films.py
            data_films = obj_actions_films.films_afficher_data()
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data films", data_films, "type ", type(data_films))
            # Différencier les messages si la table est vide.
            if data_films:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash("Données films affichées !!", "success")
            else:
                flash("""La table "t_films" est vide. !!""", "warning")
        except Exception as erreur:
            print(f"RGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGF Erreur générale. {erreur}","danger")

    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("films/films_afficher.html", data=data_films)

# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /films_add ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template"
# En cas d'erreur on affiche à nouveau la page "films_add.html"
# Pour la tester http://127.0.0.1:5005/films_add
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/films_add", methods=['GET', 'POST'])
def films_add ():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_films = GestionFilms()
            # OM 2020.04.09 Récupère le contenu du champ dans le formulaire HTML "films_add.html"
            Nom_Serv = request.form['Nom_Serv_html']
            Nombre_Port = request.form['Nombre_Port_html']
            Nombre_U = request.form['Nombre_U_html']
            Date_Conf_Serv = request.form['Date_Conf_Serv_html']
            Description = request.form['Description_html']
            Puissance = request.form['Puissance_html']
            Date_Serveur = request.form['Date_Serveur_html']
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
                            Nom_Serv):
                # OM 2019.03.28 Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "danger")
                # On doit afficher à nouveau le formulaire "films_add.html" à cause des erreurs de "claviotage"
                return render_template("films/films_add.html")
            else:

                # Constitution d'un dictionnaire et insertion dans la BD
                valeurs_insertion_dictionnaire = {"value_Nom_Serv": Nom_Serv,
                                                  "value_Nombre_Port": Nombre_Port,
                                                  "value_Nombre_U": Nombre_U,
                                                  "value_Date_Conf_Serv": Date_Conf_Serv,
                                                  "value_Description": Description,
                                                  "value_Puissance": Puissance,
                                                  "value_Date_Serveur": Date_Serveur}
                obj_actions_films.add_film_data(valeurs_insertion_dictionnaire)

                # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")
                # On va interpréter la "route" 'films_afficher', car l'utilisateur
                # doit voir le nouveau film qu'il vient d'insérer. Et on l'affiche de manière
                # à voir le dernier élément inséré.
                return redirect(url_for('films_afficher', order_by = 'DESC', id_film_sel=0))

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(
                f"RGG pei {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur:
            flash(f"Autre erreur {erreur}", "danger")
            raise MonErreur(f"Autre erreur")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except Exception as erreur:
            # OM 2020.04.09 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(
                f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']} et son status {msg_erreurs['ErreurConnexionBD']['status']}")
    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("films/films_add.html")