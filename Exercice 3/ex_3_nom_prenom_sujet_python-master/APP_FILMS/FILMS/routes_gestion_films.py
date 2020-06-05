# routes_gestion_films.py
# EZ 2020.04.27 Gestions des "routes" FLASK pour les films.

import pymysql
from flask import render_template, flash, request
from APP_FILMS import obj_mon_application
from APP_FILMS.FILMS.data_gestion_films import GestionFilms
from APP_FILMS.DATABASE.connect_db_context_manager import MaBaseDeDonnee


# OM 2020.04.16 Afficher les films
# Pour la tester http://127.0.0.1:1234/films_afficher
@obj_mon_application.route("/films_afficher")
def films_afficher():
    # OM 2020.04.09 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_films = GestionFilms()
            # Récupére les données grâce à une requête MySql définie dans la classe GestionFilms()
            # Fichier data_gestion_films.py
            data_films = obj_actions_films.films_afficher_data()
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data films", data_films, "type ", type(data_films))

            # OM 2020.04.09 La ligns ci-après permet de donner un sentiment rassurant aux utilisateurs.
            flash("Données films affichées !!", "Success")
        except Exception as erreur:
            print(f"RGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGF Erreur générale. {erreur}")

    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("films/films_afficher.html", data=data_films)


# OM 2020.04.06 Pour une simple démo. On insère deux fois des valeurs dans la table films
# Une fois de manière fixe, vous devez changer les valeurs pour voir le résultat dans la table "t_films"
# La 2ème il faut entrer la valeur du titre du films par le clavier, il ne doit pas être vide.
# Pour les autres valeurs elles doivent être changées ci-dessous.
# Une des valeurs est "None" ce qui en MySql donne "NULL" pour l'attribut "t_films.cover_link_films"
# Pour la tester http://127.0.0.1:1234/film_add

@obj_mon_application.route("/film_add", methods=['GET', 'POST'])
def film_add():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    if request.method == "POST":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_films = GestionFilms()
            # OM 2020.04.09 Récupère le contenu du champ dans le formulaire HTML "film_add.html"
            name_films = request.form['name_films_html']

            # OM 2019.04.04 On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-z\u00C0-\u00FF])[A-Za-z\u00C0-\u00FF]*['\\- ]?[A-Za-z\u00C0-\u00FF]+$",
                                name_films):
                # OM 2019.03.28 Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "Danger")
                # On doit afficher à nouveau le formulaire "film_add.html" à cause des erreurs de "claviotage"
                return render_template("films/film_add.html")
            else:

                # Constitution d'un dictionnaire et insertion dans la BD
                valeurs_insertion_dictionnaire = {"value_intitule_films": name_films}
                obj_actions_films.add_films_data(valeurs_insertion_dictionnaire)

                # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données insérées !!", "Sucess")
                print(f"Données insérées !!")
                # On va interpréter la "route" 'films_afficher', car l'utilisateur
                # doit voir le nouveau films qu'il vient d'insérer.
                return redirect(url_for('films_afficher'))

        # OM 2020.04.16 ATTENTION à l'ordre des excepts très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurDoublon(f"RGG pei {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur:
            flash(f"Autre erreur {erreur}")
            raise MonErreur(f"Autre erreur")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts très important de respecter l'ordre.
        except Exception as erreur:
            # OM 2020.04.09 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']} et son status {msg_erreurs['ErreurConnexionBD']['status']}")
    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("films/film_add.html")


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /film_edit , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un films de films par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/film_edit', methods=['POST', 'GET'])
def film_edit():
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "films_afficher.html"
    if request.method == 'GET':
        try:
            # Récupérer la valeur de "id_films" du formulaire html "films_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupére la valeur de "id_films"
            # grâce à la variable "id_film_edit_html"
            # <a href="{{ url_for('film_edit', id_film_edit_html=row.id_films) }}">Edit</a>
            id_film_edit = request.values['id_film_edit_html']

            # Pour afficher dans la console la valeur de "id_film_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(id_film_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_id_films": id_film_edit}

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_films = GestionFilms()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_films = obj_actions_films.edit_films_data(valeur_select_dictionnaire)
            print("dataIdfilms ", data_id_films, "type ", type(data_id_films))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Editer le films d'un films !!!")

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

    return render_template("films/film_edit.html", data=data_id_films)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /films_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un films de films par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------


@obj_mon_application.route('/films_update', methods=['POST', 'GET'])
def films_update():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "films_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du films alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ",request.values)

            # Récupérer la valeur de "id_films" du formulaire html "film_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupére la valeur de "id_films"
            # grâce à la variable "id_film_edit_html"
            # <a href="{{ url_for('film_edit', id_film_edit_html=row.id_films) }}">Edit</a>
            id_film_edit = request.values['id_film_edit_html']

            # Récupère le contenu du champ "intitule_films" dans le formulaire HTML "filmsEdit.html"
            name_films = request.values['name_edit_intitule_films_html']
            valeur_edit_list = [{'id_films': id_film_edit, 'intitule_films': name_films}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-z\u00C0-\u00FF])[A-Za-z\u00C0-\u00FF]*['\\- ]?[A-Za-z\u00C0-\u00FF]+$", name_films):
                # En cas d'erreur, conserve la saisie fausse, afin que l'utilisateur constate sa misérable faute
                # Récupère le contenu du champ "intitule_films" dans le formulaire HTML "filmsEdit.html"
                #name_films = request.values['name_edit_intitule_films_html']
                # Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "Danger")

                # On doit afficher à nouveau le formulaire "film_edit.html" à cause des erreurs de "claviotage"
                # Constitution d'une liste pour que le formulaire d'édition "film_edit.html" affiche à nouveau
                # la possibilité de modifier l'entrée
                # Exemple d'une liste : [{'id_films': 13, 'intitule_films': 'philosophique'}]
                valeur_edit_list = [{'id_films': id_film_edit, 'intitule_film': name_films}]

                # DEBUG bon marché :
                # Pour afficher le contenu et le type de valeurs passées au formulaire "film_edit.html"
                print(valeur_edit_list, "type ..",  type(valeur_edit_list))
                return render_template('films/film_edit.html', data=valeur_edit_list)
            else:
                # Constitution d'un dictionnaire et insertion dans la BD
                valeur_update_dictionnaire = {"value_id_films": id_film_edit, "value_name_films": name_films}

                # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
                obj_actions_films = GestionFilms()

                # La commande MySql est envoyée à la BD
                data_id_films = obj_actions_films.update_films_data(valeur_update_dictionnaire)
                # DEBUG bon marché :
                print("dataIdfilms ", data_id_films, "type ", type(data_id_films))
                # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Editer le films d'un films !!!")
                # On affiche les films
                return redirect(url_for('films_afficher'))

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:

            print(erreur.args)
            flash(f"problème films update{erreur.args[0]}")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_intitule_films_html" alors on renvoie le formulaire "EDIT"
            return render_template('films/film_edit.html', data=valeur_edit_list)

    return render_template("films/films_update.html")

@obj_mon_application.route('/films_select_delete', methods=['POST', 'GET'])
def films_select_delete():

    if request.method == 'GET':
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_films = GestionFilms()
            # OM 2019.04.04 Récupérer la valeur de "idfilmsDeleteHTML" du formulaire html "filmsDelete.html"
            id_film_delete = request.args.get('id_film_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_films": id_film_delete}


            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_films = obj_actions_films.delete_select_films_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur film_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur film_delete {erreur.args[0], erreur.args[1]}")

    # Envoie la page "HTML" au serveur.
    return render_template('films/film_delete.html', data = data_id_films)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /filmsUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un films, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/film_delete', methods=['POST', 'GET'])
def film_delete():

    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_films = GestionFilms()
            # OM 2019.04.02 Récupérer la valeur de "id_films" du formulaire html "filmsAfficher.html"
            id_film_delete = request.form['id_film_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_films": id_film_delete}

            data_films = obj_actions_films.delete_films_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des films des films
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les films
            return redirect(url_for('films_afficher'))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.04.09 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "films" de films qui est associé dans "t_films_films".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des films !')
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"IMPOSSIBLE d'effacer !! Ce films est associé à des films dans la t_films_films !!! : {erreur}")
                # Afficher la liste des films des films
                return redirect(url_for('films_afficher'))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur film_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur film_delete {erreur.args[0], erreur.args[1]}")


            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('films/film_delete.html', data=data_films)
