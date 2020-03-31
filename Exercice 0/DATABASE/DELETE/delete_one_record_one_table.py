# delete_fixe_one_rec_one_table.py
# OM 2020.03.10 le but est d'effacer une ligne d'une table en MySql


from DATABASE import connect_db

import pymysql
import warnings


# OM 2020.03.02 Mécanisme ingénieux qui filtre les warnings et les associes
# pour être traitées comme des erreurs dans le code Python.


warnings.filterwarnings(
  action="error",
  message=".*Duplicate entry.*",
  category=pymysql.Warning
)
warnings.filterwarnings(
  action="error",
  message=".*1265.*",
  category=pymysql.Warning
)

class DbDeleteOneTable():

    # Constructeur, à chaque instanciation de cette classe "DbInsertOneTable()" les lignes de code de la méthode "__init__ (self)" sont interprétées.
    def __init__ (self):  # Constructeur
        print("Constructeur CLASSE DbDeleteOneTable")



    def delete_one_record_one_table(self, requete_delete_mysql, num_ligne_delete):
        try:
            # OM 2020.01.28 CONNECTION A LA BD
            self.connection_dbc = connect_db.DatabaseTools()
            self.connection_dbc.is_connection_open()

            #self.DBcursor = connect_db.DatabaseTools.connect_ma_bd().
            # OM 2020.03.11 Execute la requête avec un passage de paramètres
            self.connection_dbc.DBcursor.execute(requete_delete_mysql, {'no_ligne_delete' : num_ligne_delete})
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.commit()
            self.connection_dbc.DBcursor.close()
        except pymysql.Error as error:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print(" Il y a une ERREUR : %s", error)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.DataError as error1:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print(" Il y a une DataError : %s", error1)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.DatabaseError as error2:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print(" Il y a une DatabaseError : %s", error2)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.Warning as error3:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print(" Il y a une Warning : %s", error3)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.MySQLError as error4:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print(" Il y a une MySQLError : %s", error4)
            print("connection_dbc.db.rollback() insertOneRecord")
        except pymysql.IntegrityError as error5:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print(" Il y a une IntegrityError : %s", error5)
            print("connection_dbc.db.rollback() insertOneRecord")
        except:
            # OM 2020.03.11 L'instruction suivante est indispensable pour confirmer l'effacement des données (en cas de problèmes : rollback)
            self.connection_dbc.db.rollback()
            print("Unknown error occurred")
        finally:
            print("C'est terminé....finally self.DBcursor.close()")
            self.connection_dbc.DBcursor.close()
