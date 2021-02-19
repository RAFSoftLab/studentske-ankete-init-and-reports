# -*- coding: utf-8 -*-

import requests
from databaseconfig import *
import json
from insert_queries import INSERTS


# response = requests.get('https://rfidis.raf.edu.rs/dbapi.php?func=predmeti')
# print(response)
# print(response.content)
#
# predmetidict = response.json()
#
# with open('predmeti1.json', 'w') as json_file:
#     json.dump(predmetidict, json_file)

nepostojeci_studenti = []

with open('predmeti1.json') as json_file:
    predmetidict = json.load(json_file)
    print('broj predmeta ')
    print(len(predmetidict))


for sifra, predmet in predmetidict.items():
    if predmet == "Diskretne strukture 1":
        predmet = "Diskretne strukture"
    if predmet == "Engleski jezik 1":
        predmet = "Engleski 1"
    if predmet == "Engleski jezik 3":
        predmet = "Engleski 3"
    if predmet == "Engleski jezik 2":
        predmet = "Engleski 2"
    if predmet == "3-D modelovanje i animacija":
        predmet = "3D modelovanje i animacija"
    if predmet == "Praktikum iz arhitekture računara i operativnih s":
        predmet = "Praktikum iz arhitekture racunara i operativnih sistema"
    if predmet ==  "Uvod u softversko inženjeerstvo":
        predmet = "Uvod u softversko inzenjerstvo"    
    try:
        query = "SELECT id_predmeta FROM predmet WHERE naziv like %s "
        cursor.execute(query, (predmet,))
        p = cursor.fetchone()
        if p is None:
            predmet = predmet.replace("<eng>","").replace("</eng>","")
            cursor.execute(INSERTS['predmet'], (predmet,))
            cnx.commit()
            id_predmeta = cursor.lastrowid
        else:
            id_predmeta = p[0]
            print(sifra)
            response = requests.get('https://rfidis.raf.edu.rs/dbapi.php?func=studenti-za-predmet&predmet=' + sifra)
            studenti = response.json()
            #print(predmet)
            #print(studenti)
        for s in studenti:
            smerbroj = s["index"].split("/")[0]
            smer = smerbroj[0:2]
            broj = smerbroj[2:]
            godina = smerbroj = s["index"].split("/")[1]
            ime = s["name"].split(" ")[0]
            prezime = s["name"].rsplit(" ",1)[1]
            nalog = prezime.lower().replace("ć", "c").replace("š", "s").replace("č", "c").replace("ž", "z").replace("đ", "dj")
            nalogindeks = "%"+nalog+broj+godina[2:] + smer.lower()+"%"
            print(nalogindeks)
            query = "SELECT id_studenta FROM student WHERE  username like %s"
            cursor.execute(query,(nalogindeks,))
            st = cursor.fetchall()
            for id_st in st:
                print(id_st[0])
                cursor.execute(INSERTS['student_predmet_semestar'], (id_st[0], id_predmeta, trenutni_semestar))
                cnx.commit()

            nalog = prezime.lower().replace("ć", "c").replace("š", "s").replace("č", "c").replace("ž", "z").replace("đ",
                                                                                                                    "dj")
            nalogstari = "%" + nalog + godina[2:]
            print(nalogstari)
            query = "SELECT id_studenta FROM student WHERE  username like %s"
            cursor.execute(query, (nalogstari,))
            st = cursor.fetchall()
            for id_st in st:
                print(id_st[0])

                cursor.execute(INSERTS['student_predmet_semestar'], (id_st[0], id_predmeta, trenutni_semestar))
                cnx.commit()
            continue




        #         nalogstari =
        #         query = "SELECT id_studenta FROM student WHERE   ime like  %s and prezime like %s"
        #         cursor.execute(query, (ime,prezime))
        #         st = cursor.fetchall()
        #         if len(st) is 0:
        #             print("Nepostojeci student --- ")
        #             nepostojeci_studenti.append((smer,broj,godina,ime,prezime))
        #
        #         else:
        #             for id_st in st:
        #                 print(id_st[0])
        #                 cursor.execute(INSERTS['student_predmet_semestar'], (id_st[0], id_predmeta, trenutni_semestar))
        #                 cnx.commit()

    except Exception as e:
        print(e)

print(nepostojeci_studenti)