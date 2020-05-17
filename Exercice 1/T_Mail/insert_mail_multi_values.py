# insert_serveur_multi_values.py
# EZ 2020.04.05 Permet d'insérer plusieurs valeurs dans la table t_films

# Importer le fichier "InsertOneTable" dans lequel il y a quelques classes et méthodes en rapport avec le sujet d'insertion dans UNE SEULE table.
from Exercice1.DATABASE.INSERT import insert_one_table

try:
    # OM 2020.01.28 Une instance "insert_records" pour permettre l'utilisation des méthodes de la classe DbInsertOneTable
    insert_records = insert_one_table.DbInsertOneTable()

    valeur_ins_1 = "Jean@dujardin.ch"
    # Afficher les valeurs dans la console...c'est tout, vraiment tout !
    print("valeur_ins_1 ",valeur_ins_1)

    # Définitions d'un dictionnaire pour passer les valeurs en paramètres de façon un "peu" sécurisée dans la BD
    valeurs_insertion_dictionnaire = {'value_Adresse_Mail': valeur_ins_1}

    # OM 2020.01.28 Pour éviter les injections SQL, il est possible de passer les valeurs à insérer sous forme "paramètrée" (avec le %(...)s au lieu de %s)
    # Pour les vrais geeks et geeketes consulter le site ci-dessous.
    # L'insertion de données est vraiment TROP inspirée du site suivant MERCI !!! https://realpython.com/prevent-python-sql-injection/

    # Une longue chaîne de caractères (format PEP8 selon proposition de PyCharm)
    # Je décide d'insèrer 3 valeurs sur 6, on voit ainsi la correspondance des positions entre les attributs
    # de la BD et les variables Python définies juste en dessus.
    mysql_insert_string = "INSERT INTO t_mail (ID_Mail, Adresse_Mail)" \
                          "VALUES (NULL, %(value_Adresse_Mail)s)"
    # Insertion des valeurs définie dans la variable dictionnaire "valeurs_insertion_dictionnaire"
    # dans la table "t_films"
    insert_records.insert_one_record_many_values_one_table(mysql_insert_string,
                                                           valeurs_insertion_dictionnaire)

except Exception as erreur:
    # OM 2020.03.01 Message en cas d'échec du bon déroulement des commandes ci-dessus.
    print("error message: {0}".format(erreur))