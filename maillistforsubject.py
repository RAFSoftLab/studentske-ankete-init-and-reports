import requests
from databaseconfig import *
import json
from insert_queries import INSERTS

if __name__ == "__main__":
    dodatih_studenata = 0
    response = requests.get('https://maillist.raf.edu.rs/api.php?func=studenti-za-predmet&predmet=08-0007a')
    content = response.content.split("><br />")
    st_data = content[len(content) - 1]
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
                print("dodavanje studenta ime=" + ime + ", prezime =" + prezime)
                print(nalog)
                dodatih_studenata += 1
                cursor.execute(INSERTS['student'], (ime, prezime, None, None, None, nalog))
                cnx.commit()
                id_st = cursor.lastrowid
            else:
                id_st = st[0][0]
                print(st)

            cursor.execute(INSERTS['student_predmet_semestar'], (id_st,54, trenutni_semestar))
            cnx.commit()
        except Exception as inst:
            print(type(inst))