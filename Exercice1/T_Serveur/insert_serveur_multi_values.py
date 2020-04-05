# insert_serveur_multi_values.py
# EZ 2020.04.05 Permet d'insérer plusieurs valeurs dans la table t_films

# Importer le fichier "InsertOneTable" dans lequel il y a quelques classes et méthodes en rapport avec le sujet d'insertion dans UNE SEULE table.
from Exercice1.DATABASE.INSERT import insert_one_table

try:
    # OM 2020.01.28 Une instance "insert_records" pour permettre l'utilisation des méthodes de la classe DbInsertOneTable
    insert_records = insert_one_table.DbInsertOneTable()

    valeur_ins_1 = "serveur1"
    valeur_ins_2 = 20
    valeur_ins_3 = 12
    valeur_ins_4 = "2020-05-15"
    valeur_ins_5 = "wesh bien ou quoi"
    valeur_ins_6 = 2500

    # Afficher les valeurs dans la console...c'est tout, vraiment tout !
    print("valeur_ins_1 ",valeur_ins_1, "valeur_ins_2 ",valeur_ins_2, "valeur_ins_3 ",valeur_ins_3, "valeur_ins_4 ",valeur_ins_4, "valeur_ins_5 ",valeur_ins_5, "valeur_ins_6 ",valeur_ins_6)

    # Définitions d'un dictionnaire pour passer les valeurs en paramètres de façon un "peu" sécurisée dans la BD
    valeurs_insertion_dictionnaire = {'value_Nom_Serv': valeur_ins_1, 'value_Nombre_Port': valeur_ins_2, 'value_Nombre_U': valeur_ins_3, 'Date_Conf_Serv': valeur_ins_4, 'value_Description': valeur_ins_5, 'value_Puissance': valeur_ins_6}

    # OM 2020.01.28 Pour éviter les injections SQL, il est possible de passer les valeurs à insérer sous forme "paramètrée" (avec le %(...)s au lieu de %s)
    # Pour les vrais geeks et geeketes consulter le site ci-dessous.
    # L'insertion de données est vraiment TROP inspirée du site suivant MERCI !!! https://realpython.com/prevent-python-sql-injection/

    # Une longue chaîne de caractères (format PEP8 selon proposition de PyCharm)
    # Je décide d'insèrer 3 valeurs sur 6, on voit ainsi la correspondance des positions entre les attributs
    # de la BD et les variables Python définies juste en dessus.
    mysql_insert_string = "INSERT INTO t_serveur (ID_Serveur, Nom_Serv, Nombre_Port, Nombre_U, Date_Conf_Serv, Description, Puissance, Date_Serveur) " \
                          "VALUES (NULL, %(value_Nom_Serv)s, %(value_Nombre_Port)s, %(value_Nombre_U)s, %(Date_Conf_Serv)s, %(value_Description)s, %(value_Puissance)s, NULL)"
    # Insertion des valeurs définie dans la variable dictionnaire "valeurs_insertion_dictionnaire"
    # dans la table "t_films"
    insert_records.insert_one_record_many_values_one_table(mysql_insert_string,
                                                           valeurs_insertion_dictionnaire)

except Exception as erreur:
    # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
    print("error message: {0}".format(erreur))