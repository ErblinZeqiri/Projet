# insert_table_values.py
# OM 2698.03.21 essai d'insertion

import connect_db
# Importer le fichier "InsertOneTable" dans lequel il y a quelques classes et méthodes en rapport avec le sujet d'insertion dans UNE SEULE table.
from INSERT import insert_one_table


try:


    # OM 202.03.11 Démonstration en classe, juste pour faire un objet "jeveux_etre_connecte"

    objet_etre_connecte = connect_db.DatabaseTools()

    # OM 2020.01.28 Une instance "insert_records" pour permettre l'utilisation des méthodes de la classe DbInsertOneTable
    insert_records = insert_one_table.DbInsertOneTable()

    valeur_debile_mais_presque_aleatoire_a_inserer = "voilà c'est tellement rose"
    print(valeur_debile_mais_presque_aleatoire_a_inserer)


    insert_records.insert_one_record_one_table("INSERT IGNORE INTO T_Type_Equipement(ID_Type_Equipement, Type_Equipement) VALUES (null, %(values_insert)s)",valeur_debile_mais_presque_aleatoire_a_inserer)



    objet_etre_connecte.close_connection()

except Exception as erreur_fatale_mais_si_jolie:
    print("la c'est grave il y a une erreur {0}".format(erreur_fatale_mais_si_jolie))

 #INSERT IGNORE INTO t_serveur(ID_Serveur, Nombre_Port, Nombre_U, Date_Conf_Serv, Description, Puissance, Date_Serveur