from __future__ import print_function
import sys
import mysql.connector
from create_queries import TABLES

from insert_queries import INSERTS

import databaseconfig as cfg

def create_database():
    try:
        for table, table_query in TABLES.items():
            cfg.cursor.execute(table_query)
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def import_questions():
    print("Importing questions...")
    with open("izmene - questions_sr.txt", "r", encoding="UTF-8") as pitanja:
        for line in pitanja:
            print("Pitanje:",line)
            lista = line.split(";")
            tekst = lista[0]
            tip = lista[1]
            format = lista[2]
            pitanje_data = (tekst, tip, format)
            try:
                cfg.cursor.execute(INSERTS['pitanje'], pitanje_data)
            except mysql.connector.Error as err:
                print(err)
                pass
    cfg.cnx.commit()

create_database()
import_questions()



