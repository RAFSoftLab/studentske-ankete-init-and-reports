# -*- coding: utf-8 -*-

def get_current_semestar(cursor):
    query = "SELECT * FROM trenutni_semestar"
    cursor.execute(query)
    for (id_semestra, skolska_godina, tip_semestra) in cursor:
        return {"skolska_godina" : skolska_godina,
                "tip_semestra" : tip_semestra}


GROUP_ID_BAZA = {}
def get_group_id(cursor, broj_grupe, trenutni_semestar):
    if broj_grupe in GROUP_ID_BAZA:
        return GROUP_ID_BAZA[broj_grupe]

    query = "SELECT id_grupe FROM grupa " \
            "JOIN semestar ON grupa.id_semestra = semestar.id_semestra AND grupa.broj = %s AND semestar.školska_godina= %s AND " \
            "semestar.tip_semestra = %s"
    cursor.execute(query, (broj_grupe, trenutni_semestar['skolska_godina'], trenutni_semestar['tip_semestra']))
    for (id_grupe, ) in cursor:
        GROUP_ID_BAZA[broj_grupe] = id_grupe
        return id_grupe


SEMESTAR_ID_BAZA = {}
def get_semestar_id(cursor, broj_grupe, trenutni_semestar):
    if broj_grupe in SEMESTAR_ID_BAZA:
        return SEMESTAR_ID_BAZA[broj_grupe]
    if broj_grupe[0] == '1':
        if trenutni_semestar['tip_semestra'] == 'zimski':
            broj_semestra = 1
        else:
            broj_semestra = 2
    elif broj_grupe[0] == '2':
        if trenutni_semestar['tip_semestra'] == 'zimski':
            broj_semestra = 3
        else:
            broj_semestra = 4
    elif broj_grupe[0] == '3':
        if trenutni_semestar['tip_semestra'] == 'zimski':
            broj_semestra = 5
        else:
            broj_semestra = 6
    elif broj_grupe[0] == '4':
        if trenutni_semestar['tip_semestra'] == 'zimski':
            broj_semestra = 7
        else:
            broj_semestra = 8
    else:   #Ponovci
        if trenutni_semestar['tip_semestra'] == 'zimski':
            broj_semestra = -1
        else:
            broj_semestra = -2

    query = "SELECT id_semestra FROM semestar " \
            "WHERE školska_godina = %s AND broj_semestra = %s"
    cursor.execute(query, (trenutni_semestar['skolska_godina'], broj_semestra))
    for (id_semestra, ) in cursor:
        SEMESTAR_ID_BAZA[broj_grupe] = id_semestra
        return id_semestra


TEACHER_ID_BAZA = {}
def get_teacher_id(cursor, ime, prezime, tip):
    if (ime, prezime, tip) in TEACHER_ID_BAZA:
        return TEACHER_ID_BAZA[(ime, prezime, tip)]
    query = "SELECT id_nastavnika FROM nastavnik " \
            "WHERE nastavnik.ime = %s AND nastavnik.prezime = %s AND nastavnik.tip = %s"
    cursor.execute(query, (ime, prezime, tip))
    for (id_nastavnika, ) in cursor:
        TEACHER_ID_BAZA[(ime, prezime, tip)] = id_nastavnika
        return id_nastavnika

COURSE_ID_BAZA = {}
def get_course_id(cursor, naziv):
    if naziv in COURSE_ID_BAZA:
        return COURSE_ID_BAZA[naziv]
    query = "SELECT id_predmeta FROM predmet " \
            "WHERE predmet.naziv = %s"
    cursor.execute(query, (naziv,))
    for (id_predmeta, ) in cursor:
        COURSE_ID_BAZA[naziv] = id_predmeta
        return id_predmeta
