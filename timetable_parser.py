# -*- coding: utf-8 -*-
from __future__ import print_function
import mysql.connector
from insert_queries import INSERTS
from getters import *
from databaseconfig import *


def import_timetable_data(path,curr_sem_id):

    with open(path, "r") as raspored:
        line_number = 0
        for line in raspored:
            print(line_number)
            line_number += 1
            row = line[1:-1].split('","')

            predmet = row[0]
            tip_casa = row[1]
            if (tip_casa == 'Predavanja'):
                tip = 'Profesor'
            elif (tip_casa == 'Vezbe'):
                tip = 'Asistent'
            elif (tip_casa == 'Praktikum'):   # Laboratorijske vezbe
                tip = 'Saradnik'
            nastavnik = row[2]
            poz = nastavnik.rfind(" ")
            prezime = nastavnik[:poz]
            ime = nastavnik[poz+1:]
            pemail = prezime.lower().replace(" ", "")
            email = ime.lower()[0:1] + pemail + "@raf.rs"
            grupe = row[3]
            grupe_lista = [x.strip() for x in grupe.split(",")]

            predmet_data = (predmet, )
            # da li se predmet vec nalazi u bazi
            cursor.execute("SELECT * FROM predmet where naziv like %s",(predmet,))
            cursor.fetchall()
            if cursor.rowcount == 0:
                try:
                    cursor.execute(INSERTS['predmet'], predmet_data)
                except mysql.connector.Error as err:
                    print(err)
                    pass

            nastavnik_data = (ime, prezime, tip, email)
            # da li se nastavnik vec nalazi u bazi
            cursor.execute("SELECT * FROM nastavnik where ime like %s and prezime like %s and tip like %s", (ime, prezime, tip))
            cursor.fetchall()
            if cursor.rowcount == 0:
                try:
                    cursor.execute(INSERTS['nastavnik'], nastavnik_data)
                except mysql.connector.Error as err:
                    pass


            id_nastavnika = get_teacher_id(cursor, ime, prezime, tip)
            id_predmeta = get_course_id(cursor, predmet)

            for grupa in grupe_lista:
                drzi_predmet_data = (id_nastavnika, id_predmeta, grupa, curr_sem_id)
                try:
                    cursor.execute(INSERTS['drzi_predmet'], drzi_predmet_data)
                except mysql.connector.Error as err:
                    print(err)
                    pass

    cnx.commit()
    cnx.close()

