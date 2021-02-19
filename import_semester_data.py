from insert_queries import INSERTS
from databaseconfig import *
import sys
import timetable_parser as tp
import os

# example usage: python import_semester_data.py "2020/2021" z csv
# csv - fajl sa rasporedom za semestar
if __name__ == "__main__":
    skolska_godina = sys.argv[1]
    semestar = sys.argv[2]   # z ili l (zimski ili letnji)
    raspored_path = sys.argv[3]

    if not(os.path.exists(raspored_path)):
        print("Ne postoji fajl na putanji: ",raspored_path)
        exit()

    # insert current semester
    print("Inserting current semester data:", skolska_godina, semestar)

    semestar_data = (skolska_godina,semestar)

    cursor.execute(INSERTS['semestar'], semestar_data)
    semester_id = cursor.lastrowid
    print("Semester id =", semester_id)
    cnx.commit()

    tp.import_timetable_data(raspored_path, semester_id)

