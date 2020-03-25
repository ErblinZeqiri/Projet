# insert_genres_one_value.py
# OM 2698.03.21 essai d'insertion

from DATABASE import connect_db
# Importer le fichier "InsertOneTable" dans lequel il y a quelques classes et méthodes en rapport avec le sujet d'insertion dans UNE SEULE table.
from DATABASE.INSERT import insert_one_table

#  OM 2020.03.11 Indispensable en cas de problèmes, gérer les erreurs en informatique
try:

    # OM 202.03.11 Démonstration en classe, juste pour "faire" un objet "objet_etre_connecte" (instancier la classe)
    connection_dbc = connect_db.DatabaseTools()

    # OM 2020.01.28 Une instance "insert_records" pour permettre l'utilisation des méthodes de la classe DbInsertOneTable
    insert_records = insert_one_table.DbInsertOneTable()

    valeur_debile_mais_presque_aleatoire_a_inserer = "grosse crocoll"
    # Ligne pour afficher la valeur dans la console...c'est tout
    print(valeur_debile_mais_presque_aleatoire_a_inserer)

    # OM 2020.01.28 Pour éviter les injections SQL, il est possible de passer les valeurs à insérer sous forme "paramètrée" (avec le %(...)s au lieu de %s)
    # Pour les vrais geeks et geeketes consulter le site ci-dessous.
    # L'insertion de données est vraiment TROP inspirée du site suivant MERCI !!! https://realpython.com/prevent-python-sql-injection/
    # Dans la requête SQL le mot clé IGNORE est là pour TRANSFORMER une erreur SQL en une WARNING
    mysql_insert_string = "INSERT IGNORE INTO t_genres (id_genre, intitule_genre) VALUES (null, %(values_insert)s)"

    # Insertion de la valeur définie dans la variable "valeur_debile_mais_presque_aleatoire_a_inserer"
    # dans la table "t_genres"
    insert_records.insert_one_record_one_table(mysql_insert_string,
                                               valeur_debile_mais_presque_aleatoire_a_inserer)
    # Ferme la connection à la BD
    connection_dbc.close_connection()
    # OM 2020.01.28 C'est un simple test, pour savoir si la BD est bien fermée.
    connection_dbc.is_connection_open()

except Exception as erreur:
    print("Message erreur {0}".format(erreur))