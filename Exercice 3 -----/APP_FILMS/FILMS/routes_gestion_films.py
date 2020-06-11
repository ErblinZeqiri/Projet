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

# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /films_edit ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un film de films par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/films_edit', methods=['POST', 'GET'])
def films_edit ():
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "films_afficher.html"
    if request.method == 'GET':
        try:
            # Récupère la valeur de "id_film" du formulaire html "films_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "id_film"
            # grâce à la variable "id_film_edit_html"
            # <a href="{{ url_for('films_edit', id_film_edit_html=row.id_film) }}">Edit</a>
            id_film_edit = request.values['id_film_edit_html']

            # Pour afficher dans la console la valeur de "id_film_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(id_film_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_ID_Serveur": id_film_edit}

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_films = GestionFilms()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_film = obj_actions_films.edit_film_data(valeur_select_dictionnaire)
            print("dataIdfilm ", data_id_film, "type ", type(data_id_film))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Editer le film d'un film !!!", "success")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:

            # On indique un problème, mais on ne dit rien en ce qui concerne la résolution.
            print("Problème avec la BD ! : %s", erreur)
            # OM 2020.04.09 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']}"
                                      f"et son status {msg_erreurs['ErreurConnexionBD']['status']}")

    return render_template("films/films_edit.html", data=data_id_film)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /films_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un film de films par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/films_update', methods=['POST', 'GET'])
def films_update ():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "films_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du film alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ", request.values)

            # Récupère la valeur de "id_film" du formulaire html "films_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupère la valeur de "id_film"
            # grâce à la variable "id_film_edit_html"
            # <a href="{{ url_for('films_edit', id_film_edit_html=row.id_film) }}">Edit</a>
            id_film_edit = request.values['id_film_edit_html']

            # Récupère le contenu du champ "intitule_film" dans le formulaire HTML "filmsEdit.html"
            Nom_Serv = request.values['name_edit_Nom_Serv_html']
            Nombre_Port = request.values['name_edit_Nombre_Port_html']
            Nombre_U = request.values['name_edit_Nombre_U_html']
            Date_Conf_Serv = request.values['name_edit_Date_Conf_Serv_html']
            Description = request.values['name_edit_Description_html']
            Puissance = request.values['name_edit_Puissance_html']

            valeur_edit_list = [{'ID_Serveur': id_film_edit,
                                 'Nom_Serv': Nom_Serv,
                                 'Nombre_Port': Nombre_Port,
                                 'Nombre_U': Nombre_U,
                                 'Date_Conf_Serv': Date_Conf_Serv,
                                 'Description': Description,
                                 'Puissance': Puissance}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.v
            if not re.match("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
                            Nom_Serv):
                # En cas d'erreur, conserve la saisie fausse, afin que l'utilisateur constate sa misérable faute
                # Récupère le contenu du champ "intitule_film" dans le formulaire HTML "filmsEdit.html"
                # Nom_Serv = request.values['name_edit_intitule_film_html']
                # Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "danger")

                # On doit afficher à nouveau le formulaire "films_edit.html" à cause des erreurs de "claviotage"
                # Constitution d'une liste pour que le formulaire d'édition "films_edit.html" affiche à nouveau
                # la possibilité de modifier l'entrée
                # Exemple d'une liste : [{'id_film': 13, 'intitule_film': 'philosophique'}]
                valeur_edit_list = [{'ID_Serveur': id_film_edit,
                                     'Nom_Serv': Nom_Serv,
                                     'Nombre_Port': Nombre_Port,
                                     'Nombre_U': Nombre_U,
                                     'Date_Conf_Serv': Date_Conf_Serv,
                                     'Description': Description,
                                     'Puissance': Puissance}]

                # DEBUG bon marché :
                # Pour afficher le contenu et le type de valeurs passées au formulaire "films_edit.html"
                print(valeur_edit_list, "type ..", type(valeur_edit_list))
                return render_template('films/films_edit.html', data=valeur_edit_list)
            else:
                # Constitution d'un dictionnaire et insertion dans la BD
                valeur_update_dictionnaire = {"value_ID_Serveur": id_film_edit,
                                              "value_Nom_Serv": Nom_Serv,
                                              "value_Nombre_Port": Nombre_Port,
                                              "value_Nombre_U": Nombre_U,
                                              "value_Date_Conf_Serv": Date_Conf_Serv,
                                              "value_Description": Description,
                                              "value_Puissance": Puissance}

                # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
                obj_actions_films = GestionFilms()

                # La commande MySql est envoyée à la BD
                data_id_film = obj_actions_films.update_film_data(valeur_update_dictionnaire)
                # DEBUG bon marché :
                print("dataIdfilm ", data_id_film, "type ", type(data_id_film))
                # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Valeur film modifiée. ", "success")
                # On affiche les films avec celui qui vient d'être edité en tête de liste. (DESC)
                return redirect(url_for('films_afficher', order_by="ASC", id_film_sel=id_film_edit))

        except (Exception,
                # pymysql.err.OperationalError,
                # pymysql.ProgrammingError,
                # pymysql.InternalError,
                # pymysql.IntegrityError,
                TypeError) as erreur:
            print(erreur.args[0])
            flash(f"problème films ____lllupdate{erreur.args[0]}", "danger")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_intitule_film_html" alors on renvoie le formulaire "EDIT"
    return render_template('films/films_edit.html', data=valeur_edit_list)

# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /films_select_delete , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un film de films par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/films_select_delete', methods=['POST', 'GET'])
def films_select_delete ():
    if request.method == 'GET':
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_films = GestionFilms()
            # OM 2019.04.04 Récupère la valeur de "idfilmDeleteHTML" du formulaire html "filmsDelete.html"
            ID_Serveur_delete = request.args.get('ID_Serveur_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_ID_Serveur": ID_Serveur_delete}

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_ID_Serveur = obj_actions_films.delete_select_film_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!", "warning")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur films_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur films_delete {erreur.args[0], erreur.args[1]}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template('films/films_delete.html', data=data_ID_Serveur)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /filmsUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un film, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/films_delete', methods=['POST', 'GET'])
def films_delete ():
    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_films = GestionFilms()
            # OM 2019.04.02 Récupère la valeur de "id_film" du formulaire html "filmsAfficher.html"
            ID_Serveur_delete = request.form['ID_Serveur_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_ID_Serveur": ID_Serveur_delete}

            data_films = obj_actions_films.delete_film_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des films des films
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les films
            return redirect(url_for('films_afficher',order_by="ASC",id_film_sel=0))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.04.09 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "film" de films qui est associé dans "t_films_films".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des films !', "warning")
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce film est associé à des films dans la t_films_films !!! : {erreur}")
                # Afficher la liste des films des films
                return redirect(url_for('films_afficher', order_by="ASC", id_film_sel=0))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur films_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur films_delete {erreur.args[0], erreur.args[1]}", "danger")

            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('films/films_afficher.html', data=data_films)
