# routes_gestion_personnes_mails.py
# OM 2020.04.16 Gestions des "routes" FLASK pour la table intermédiaire qui associe les mails et les personnes.

from flask import render_template, request, flash, session
from APP_FILMS import obj_mon_application
from APP_FILMS.Demandeurs.data_gestion_demandeurs import GestionPersonnes
from APP_FILMS.Personnes_Mails.data_gestion_personnes_mails import GestionPersonnesMails


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.26 Définition d'une "route" /personnes_mails_afficher_concat
# Récupère la liste de tous les mails et de tous les personnes associés aux mails.
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/personnes_mails_afficher_concat/<int:id_mail_sel>", methods=['GET', 'POST'])
def personnes_mails_afficher_concat (id_mail_sel):
    print("id_mail_sel ", id_mail_sel)
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personnes = GestionPersonnesMails()
            # Récupère les données grâce à une requête MySql définie dans la classe Gestionpersonnes()
            # Fichier data_gestion_mails.py
            data_personnes_mails_afficher_concat = obj_actions_personnes.personnes_mails_afficher_data_concat(id_mail_sel)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data personnes", data_personnes_mails_afficher_concat, "type ", type(data_personnes_mails_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_personnes_mails_afficher_concat:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données personnes affichés dans PersonnesMails!!", "success")
            else:
                flash(f"""Le mail demandé n'existe pas. Ou la table "t_personnes_mails" est vide. !!""", "warning")
        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.21 Envoie la page "HTML" au mail.
    return render_template("personnes_mails/personnes_mails_afficher.html",
                           data=data_personnes_mails_afficher_concat)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.21 Définition d'une "route" /gf_edit_personne_mail_selected
# Récupère la liste de tous les personnes du mail sélectionné.
# Nécessaire pour afficher tous les "TAGS" des personnes, ainsi l'utilisateur voit les personnes à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_edit_personne_mail_selected", methods=['GET', 'POST'])
def gf_edit_personne_mail_selected ():
    if request.method == "GET":
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personnes = GestionPersonnes()
            # Récupère les données grâce à une requête MySql définie dans la classe GestionPersonne()
            # Fichier data_gestion_mails.py
            # Pour savoir si la table "t_personnes" est vide, ainsi on empêche l’affichage des tags
            # dans le render_template(personnes_mails_modifier_tags_dropbox.html)
            data_personnes_all = obj_actions_personnes.personnes_afficher_data('ASC', 0)

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données de la table intermédiaire.
            obj_actions_personnes = GestionPersonnesMails()

            # OM 2020.04.21 Récupère la valeur de "id_mail" du formulaire html "personnes_mails_afficher.html"
            # l'utilisateur clique sur le lien "Modifier personnes de ce mail" et on récupère la valeur de "id_mail" grâce à la variable "id_mail_personnes_edit_html"
            # <a href="{{ url_for('gf_edit_personne_mail_selected', id_mail_personnes_edit_html=row.id_mail) }}">Modifier les personnes de ce mail</a>
            id_mail_personnes_edit = request.values['id_mail_personnes_edit_html']

            # OM 2020.04.21 Mémorise l'id du mail dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_mail_personnes_edit'] = id_mail_personnes_edit

            # Constitution d'un dictionnaire pour associer l'id du mail sélectionné avec un nom de variable
            valeur_id_mail_selected_dictionnaire = {"value_id_mail_selected": id_mail_personnes_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la classe GestionPersonnesMailss()
            # 1) Sélection du mail choisi
            # 2) Sélection des personnes "déjà" attribués pour le mail.
            # 3) Sélection des personnes "pas encore" attribués pour le mail choisi.
            # Fichier data_gestion_personnes_mails.py
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "personnes_mails_afficher_data"
            data_personne_mail_selected, data_personnes_mails_non_attribues, data_personnes_mails_attribues = \
                obj_actions_personnes.personnes_mails_afficher_data(valeur_id_mail_selected_dictionnaire)

            lst_data_mail_selected = [item['ID_Mail'] for item in data_personne_mail_selected]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_mail_selected  ", lst_data_mail_selected,
                  type(lst_data_mail_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les personnes qui ne sont pas encore sélectionnés.
            lst_data_personnes_mails_non_attribues = [item['ID_Personne'] for item in data_personnes_mails_non_attribues]
            session['session_lst_data_personnes_mails_non_attribues'] = lst_data_personnes_mails_non_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_personnes_mails_non_attribues  ", lst_data_personnes_mails_non_attribues,
                  type(lst_data_personnes_mails_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les personnes qui sont déjà sélectionnés.
            lst_data_personnes_mails_old_attribues = [item['ID_Personne'] for item in data_personnes_mails_attribues]
            session['session_lst_data_personnes_mails_old_attribues'] = lst_data_personnes_mails_old_attribues
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_data_personnes_mails_old_attribues  ", lst_data_personnes_mails_old_attribues,
                  type(lst_data_personnes_mails_old_attribues))

            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data data_personne_mail_selected", data_personne_mail_selected, "type ", type(data_personne_mail_selected))
            print(" data data_personnes_mails_non_attribues ", data_personnes_mails_non_attribues, "type ",
                  type(data_personnes_mails_non_attribues))
            print(" data_personnes_mails_attribues ", data_personnes_mails_attribues, "type ",
                  type(data_personnes_mails_attribues))

            # Extrait les valeurs contenues dans la table "t_personnes", colonne "intitule_personne"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_personne
            lst_data_personnes_mails_non_attribues = [item['Nom_Pers'] for item in data_personnes_mails_non_attribues]
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print("lst_all_personnes gf_edit_personne_mail_selected ", lst_data_personnes_mails_non_attribues,
                  type(lst_data_personnes_mails_non_attribues))

            # Différencier les messages si la table est vide.
            if lst_data_mail_selected == [None]:
                flash(f"""Le mail demandé n'existe pas. Ou la table "t_personnes_mails" est vide. !!""", "warning")
            else:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données personnes affichées dans personnesmails!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # OM 2020.04.21 Envoie la page "HTML" au mail.
    return render_template("personnes_mails/personnes_mails_modifier_tags_dropbox.html",
                           data_personnes=data_personnes_all,
                           data_mail_selected=data_personne_mail_selected,
                           data_personnes_attribues=data_personnes_mails_attribues,
                           data_personnes_non_attribues=data_personnes_mails_non_attribues)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.26 Définition d'une "route" /gf_update_personne_mail_selected
# Récupère la liste de tous les personnes du mail sélectionné.
# Nécessaire pour afficher tous les "TAGS" des personnes, ainsi l'utilisateur voit les personnes à disposition
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/gf_update_personne_mail_selected", methods=['GET', 'POST'])
def gf_update_personne_mail_selected ():
    if request.method == "POST":
        try:
            # Récupère l'id du mail sélectionné
            id_mail_selected = session['session_id_mail_personnes_edit']
            print("session['session_id_mail_personnes_edit'] ", session['session_id_mail_personnes_edit'])

            # Récupère la liste des personnes qui ne sont pas associés au mail sélectionné.
            old_lst_data_personnes_mails_non_attribues = session['session_lst_data_personnes_mails_non_attribues']
            print("old_lst_data_personnes_mails_non_attribues ", old_lst_data_personnes_mails_non_attribues)

            # Récupère la liste des personnes qui sont associés au mail sélectionné.
            old_lst_data_personnes_mails_attribues = session['session_lst_data_personnes_mails_old_attribues']
            print("old_lst_data_personnes_mails_old_attribues ", old_lst_data_personnes_mails_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme personnes dans le composant "tags-selector-tagselect"
            # dans le fichier "personnes_mails_modifier_tags_dropbox.html"
            new_lst_str_personnes_mails = request.form.getlist('name_select_tags')
            print("new_lst_str_personnes_mails ", new_lst_str_personnes_mails)

            # OM 2020.04.29 Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_personnes_mails_old = list(map(int, new_lst_str_personnes_mails))
            print("new_lst_personnes_mails ", new_lst_int_personnes_mails_old, "type new_lst_personnes_mails ",
                  type(new_lst_int_personnes_mails_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2020.04.29 Une liste de "id_personne" qui doivent être effacés de la table intermédiaire "t_personnes_mails".
            lst_diff_personnes_delete_b = list(
                set(old_lst_data_personnes_mails_attribues) - set(new_lst_int_personnes_mails_old))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_personnes_delete_b ", lst_diff_personnes_delete_b)

            # OM 2020.04.29 Une liste de "id_personne" qui doivent être ajoutés à la BD
            lst_diff_personnes_insert_a = list(
                set(new_lst_int_personnes_mails_old) - set(old_lst_data_personnes_mails_attribues))
            # DEBUG bon marché : Pour afficher le résultat de la liste.
            print("lst_diff_personnes_insert_a ", lst_diff_personnes_insert_a)

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_personnes = GestionPersonnesMails()

            # Pour le mail sélectionné, parcourir la liste des personnes à INSÉRER dans la "t_personnes_mails".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_personne_ins in lst_diff_personnes_insert_a:
                # Constitution d'un dictionnaire pour associer l'id du mail sélectionné avec un nom de variable
                # et "id_personne_ins" (l'id du personne dans la liste) associé à une variable.
                valeurs_mail_sel_personne_sel_dictionnaire = {"value_fk_mail": id_mail_selected,
                                                           "value_fk_personne": id_personne_ins}
                # Insérer une association entre un(des) personne(s) et le mail sélectionner.
                obj_actions_personnes.personnes_mails_add(valeurs_mail_sel_personne_sel_dictionnaire)

            # Pour le mail sélectionné, parcourir la liste des personnes à EFFACER dans la "t_personnes_mails".
            # Si la liste est vide, la boucle n'est pas parcourue.
            for id_personne_del in lst_diff_personnes_delete_b:
                # Constitution d'un dictionnaire pour associer l'id du mail sélectionné avec un nom de variable
                # et "id_personne_del" (l'id du personne dans la liste) associé à une variable.
                valeurs_mail_sel_personne_sel_dictionnaire = {"value_fk_mail": id_mail_selected,
                                                           "value_fk_personne": id_personne_del}
                # Effacer une association entre un(des) personne(s) et le mail sélectionner.
                obj_actions_personnes.personnes_mails_delete(valeurs_mail_sel_personne_sel_dictionnaire)

            # Récupère les données grâce à une requête MySql définie dans la classe GestionPersonne()
            # Fichier data_gestion_mails.py
            # Afficher seulement le mail dont les personnes sont modifiés, ainsi l'utilisateur voit directement
            # les changements qu'il a demandés.
            data_personnes_mails_afficher_concat = obj_actions_personnes.personnes_mails_afficher_data_concat(id_mail_selected)
            # DEBUG bon marché : Pour afficher le résultat et son type.
            print(" data personnes", data_personnes_mails_afficher_concat, "type ", type(data_personnes_mails_afficher_concat))

            # Différencier les messages si la table est vide.
            if data_personnes_mails_afficher_concat == None:
                flash(f"""Le mail demandé n'existe pas. Ou la table "t_personnes_mails" est vide. !!""", "warning")
            else:
                # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données personnes affichées dans personnesmails!!", "success")

        except Exception as erreur:
            print(f"RGGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGGF Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Après cette mise à jour de la table intermédiaire "t_personnes_mails",
    # on affiche les mails et le(urs) personne(s) associé(s).
    return render_template("personnes_mails/personnes_mails_afficher.html",
                           data=data_personnes_mails_afficher_concat)
