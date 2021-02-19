import requests
from databaseconfig import *
import json
from insert_queries import INSERTS
import sys, os

# snima fajl predmeti.json  koji sadrži sve predmete za koje postoji mejllista
def fetch_predmeti(maillist_api_predmeti):
    response = requests.get(maillist_api_predmeti)
    print(response)
    print(response.content)

    predmeti = response.content.decode().split(",")
    for p in predmeti:
        print(p)
        parts = p.split(":")

    data = response.json()
    with open('predmeti.json', 'w') as json_file:
        json.dump(data, json_file)


if __name__ == "__main__":

    maillist_api_predmeti = sys.argv[1]
    maillist_api_prijavljeni_predmet= sys.argv[2]

    if not os.path.exists("predmeti.json"):
        fetch_predmeti(maillist_api_predmeti)

    with open('predmeti.json') as json_file:
        data = json.load(json_file)

    nepostoji_count = 0

    nepostojeci_predmeti = []

    query = "SELECT id_predmeta, naziv FROM predmet where id_predmeta in (select id_predmeta from c8_rafanketa.drzi_predmet where id_semestra = %s)"
    cursor.execute(query, (trenutni_semestar,))
    predmetiSem = cursor.fetchall()
    for predmet in predmetiSem:
        sifreZaPredmet = []
        nadjen = 0;
        for key, value in data.items():
           if value.startswith(predmet[1]):
               sifreZaPredmet.append(key)
               nadjen = 1
        if not nadjen:
            nepostojeci_predmeti.append(predmet)
            nepostoji_count+=1
        print(predmet," sifre: ",sifreZaPredmet)
        for sifra in sifreZaPredmet:
            if predmet is not None:
                id_predmeta = predmet[0]
                response = requests.get(maillist_api_prijavljeni_predmet+sifra)
                content = response.content.decode().split("><br />")
                st_data = content[len(content)-1]
                try:
                    studenti_data = json.loads(st_data)
                    for student in studenti_data:
                        try:
                            nalog = student['mail'].split("@")[0]
                            print(nalog)
                            query = "SELECT id_studenta FROM student WHERE username like %s "
                            cursor.execute(query, (nalog,))
                            st = cursor.fetchall()
                            id_st = 0
                            if len(st) is 0:
                                imeiprezime = student['name'].split(' ', 1)
                                if len(imeiprezime) is 2:
                                    ime = imeiprezime[0]
                                    prezime = imeiprezime[1]
                                else:
                                     ime = student['name']
                                print("dodavanje studenta ime="+ime+", prezime ="+prezime)
                                print(nalog)
                                cursor.execute(INSERTS['student'], (ime, prezime, None, None, None, nalog))
                                cnx.commit()
                                id_st = cursor.lastrowid
                            else:
                                id_st = st[0][0]
                                print(st)

                            cursor.execute(INSERTS['student_predmet_semestar'], (id_st, id_predmeta, trenutni_semestar))
                            cnx.commit()
                        except Exception as inst:
                            print(inst)
                except Exception as e:
                       print(e)


    print("Ukupno nepostojecih")
    print(nepostoji_count)
    print(nepostojeci_predmeti)



