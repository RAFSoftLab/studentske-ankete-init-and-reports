
from databaseconfig import *

pitanja_min = "82"
pitanje_id_nastavnik = 127
pitanje_id_predmet = 111

def get_total_count():
    query = "SELECT count(*) FROM zakljucena WHERE id_semestra = '%i'" % (trenutni_semestar)
    cursor.execute(query)
    for (count, ) in cursor:
        return count

def get_faculty_questions_reports():
    query = "SELECT id_pitanja, tekst FROM pitanje WHERE tip='fakultet' AND format='ocena' AND id_pitanja>="+pitanja_min

    cursor.execute(query)
    pitanja = []
    for (id_pitanja, tekst) in cursor:
        pitanja.append((id_pitanja, tekst))
    izvestaj_global = {}
    for (id_pitanja, tekst) in pitanja:
        izvestaj = dict()
        # prosecna ocena
        query = "SELECT AVG(odgovor) FROM odgovor_fakultet " \
                "WHERE id_semestra = %s AND id_pitanja = %s and odgovor in (1,2,3,4,5) "
        cursor.execute(query, (trenutni_semestar, id_pitanja))
        for (avg,) in cursor:
            izvestaj['prosecna_ocena'] = avg

        opcije = ['1','2','3','4','5','x']
        broj_glasova = dict.fromkeys(opcije,0)  # [0, 0, 0, 0, 0, 0, 0]
        for opcija in opcije:
            query = "SELECT COUNT(*) FROM odgovor_fakultet "\
                    "WHERE odgovor_fakultet.id_semestra = %s "\
                    "AND id_pitanja = %s AND odgovor_fakultet.odgovor = %s"
            cursor.execute(query, (trenutni_semestar, id_pitanja, opcija))
            for (count, ) in cursor:
                broj_glasova[opcija] = count
        suma = sum(broj_glasova.values())

        for opcija in opcije:
            izvestaj[opcija] = {"broj_glasova": broj_glasova[opcija],
                                    "procenat": (int) (broj_glasova[opcija] * 100 / float(suma))}

            izvestaj["ukupno"] = sum(broj_glasova.values())
           # print(izvestaj)
            izvestaj_global[tekst] = izvestaj


    return izvestaj_global

def get_option_questions_fakultet():
    # pitanja sa ponudjenim opcijama
    izvestaj_global = {}

    query = "SELECT id_pitanja, tekst, format FROM pitanje WHERE tip ='fakultet' AND format not like 'ocena' AND format not like 'tekst' AND id_pitanja>="+pitanja_min
    cursor.execute(query)
    pitanja = []
    for (id_pitanja, tekst, format) in cursor:
        pitanja.append((id_pitanja, tekst, format))
    for (id_pitanja, tekst, format) in pitanja:
        izvestaj = dict()
        opcije = format.split('|')
        broj_glasova = dict.fromkeys(opcije, 0)
        for opcija in opcije:
            query = "SELECT COUNT(*) FROM odgovor_fakultet " \
                    "WHERE odgovor_fakultet.id_semestra = %s " \
                    "AND id_pitanja = %s AND odgovor_fakultet.odgovor like %s"
            cursor.execute(query, (trenutni_semestar, id_pitanja, opcija))
            for (count,) in cursor:
                broj_glasova[opcija] = count
        suma = sum(broj_glasova.values())

        for opcija in opcije:
            izvestaj[opcija] = {"broj_glasova": broj_glasova[opcija],
                                "procenat": (int)(broj_glasova[opcija] * 100 / float(suma))}
            izvestaj["ukupno"] = sum(broj_glasova.values())
            izvestaj_global[tekst] = izvestaj

    return izvestaj_global

def get_faculty_primedbe():
    query = "SELECT f.odgovor, p.tekst FROM odgovor_fakultet f,pitanje p WHERE p.tip='fakultet' "\
            "AND p.format='tekst' AND f.id_pitanja=p.id_pitanja "\
            "AND f.id_semestra = %i" % (trenutni_semestar)
    cursor.execute(query)
    rez = dict()
    for(odgovor,tekst) in cursor:
        if tekst not in rez:
            rez[tekst] = [odgovor]
        else:
            rez[tekst].append(odgovor)
    return rez

def get_all_subjects():
    query = "SELECT p.id_predmeta,p.naziv FROM predmet p"
    cursor.execute(query)
    ret_val = dict()
    for (id_predmeta, naziv) in cursor:
        ret_val[naziv] = id_predmeta
    return ret_val

def get_subject_question_report(id):
    query = "SELECT id_pitanja, tekst FROM pitanje WHERE tip='predmet' AND format='ocena' AND id_pitanja>="+pitanja_min
    cursor.execute(query)
    pitanja = []
    for (id_pitanja, tekst) in cursor:
        pitanja.append((id_pitanja, tekst))
    izvestaj_global = {}
    for (id_pitanja, tekst) in pitanja:
        izvestaj = dict()
        # prosecna ocena
        query = "SELECT AVG(odgovor) FROM odgovor_predmet " \
                "WHERE id_semestra = %s AND id_pitanja = %s "\
                "AND id_predmeta = %s AND odgovor in (1,2,3,4,5) "
        cursor.execute(query, (trenutni_semestar, id_pitanja,id))
        for (avg,) in cursor:
            izvestaj['prosecna_ocena'] = avg

        opcije = ['1', '2', '3', '4', '5', 'x']
        broj_glasova = dict.fromkeys(opcije, 0)
        for opcija in opcije:
            query = "SELECT COUNT(*) FROM odgovor_predmet " \
                    "WHERE odgovor_predmet.id_semestra = %s " \
                    "AND id_pitanja = %s AND odgovor_predmet.odgovor = %s " \
                    "AND id_predmeta = %s"
            cursor.execute(query, (trenutni_semestar, id_pitanja, opcija,id))
            for (count,) in cursor:
                broj_glasova[opcija] = count
        suma = sum(broj_glasova.values())

        for opcija in opcije:
            if suma is not 0:
                izvestaj[opcija] = {"broj_glasova": broj_glasova[opcija],
                                        "procenat": ((int)(broj_glasova[opcija] * 100 / float(suma)))}
                izvestaj["ukupno"] = sum(broj_glasova.values())
                izvestaj_global[tekst] = izvestaj
    return izvestaj_global

def get_option_questions_subject(id):
    # pitanja sa ponudjenim opcijama
    izvestaj_global = {}

    query = "SELECT id_pitanja, tekst, format FROM pitanje WHERE tip ='predmet' AND format not like 'ocena' AND format not like 'tekst' AND id_pitanja>="+pitanja_min
    cursor.execute(query)
    pitanja = []
    for (id_pitanja, tekst, format) in cursor:
        pitanja.append((id_pitanja, tekst, format))
    for (id_pitanja, tekst, format) in pitanja:
        izvestaj = dict()
        opcije = format.split('|')
        broj_glasova = dict.fromkeys(opcije, 0)
        for opcija in opcije:
            query = "SELECT COUNT(*) FROM odgovor_predmet " \
                    "WHERE odgovor_predmet.id_semestra = %s " \
                    "AND id_pitanja = %s AND odgovor_predmet.odgovor = %s " \
                    "AND id_predmeta = %s"
            cursor.execute(query, (trenutni_semestar, id_pitanja, opcija,id))
            for (count,) in cursor:
                broj_glasova[opcija] = count
        suma = sum(broj_glasova.values())

        for opcija in opcije:
            izvestaj[opcija] = {"broj_glasova": broj_glasova[opcija],
                                "procenat": (int)(broj_glasova[opcija] * 100 / float(suma)) if suma is not 0 else 0}
            izvestaj["ukupno"] = sum(broj_glasova.values())
            izvestaj_global[tekst] = izvestaj

    return izvestaj_global

# ukupna prosevna ocena za nastavnika na predmetu
def get_teacher_avg(id_nastavnika,id_predmeta):
    query = "SELECT avg(odg.odgovor) FROM odgovor_nastavnik odg, drzi_predmet dp, pitanje p " \
            "where odg.id_drzi_predmet = dp.id and dp.id_nastavnika = %s and odg.id_pitanja = p.id_pitanja and p.format = 'ocena' and odgovor in (1,2,3,4,5) " \
            "and odg.id_semestra = %s and dp.id_predmeta = %s and p.id_pitanja>="+pitanja_min

    cursor.execute(query, (id_nastavnika,trenutni_semestar, id_predmeta))
    row = cursor.fetchone()

    if row == None:
        return (0,0)
    else:
        avg = "{0:.2f}".format(row[0])
    query = "SELECT count(odg.odgovor) FROM odgovor_nastavnik odg, drzi_predmet dp, pitanje p " \
            "where odg.id_drzi_predmet = dp.id and dp.id_nastavnika = %s and odg.id_pitanja = p.id_pitanja and p.format = 'ocena' " \
            "and odg.id_semestra = %s and dp.id_predmeta = %s AND odgovor in (1,2,3,4,5) and p.id_pitanja>="+pitanja_min
    cursor.execute(query, (id_nastavnika, trenutni_semestar, id_predmeta))
    br = cursor.fetchone()
    return (avg,str(int(br[0]/11)))  # podeljeno sa brojem pitanja ???

# ukupna prosecna ocena za predmet
def get_subject_avg(id):
    query = "SELECT avg(odgovor) FROM odgovor_predmet odg, pitanje p " \
            "where odg.id_predmeta = %s and odg.id_pitanja = p.id_pitanja and p.format = 'ocena' and odg.id_semestra = %s AND odgovor in (1,2,3,4,5) and p.id_pitanja>="+pitanja_min
    cursor.execute(query, (id,trenutni_semestar))
    row = cursor.fetchone()
    if row == None:
        return 0
    else:
        #avg = str(""row[0])
        avg = "{0:.2f}".format(row[0])
    query = "SELECT count(odgovor) FROM odgovor_predmet odg, pitanje p " \
            "where odg.id_predmeta = %s and odg.id_pitanja = p.id_pitanja and p.format = 'ocena' and odg.id_semestra = %s and p.id_pitanja>="+pitanja_min
    cursor.execute(query, (id, trenutni_semestar))
    br = cursor.fetchone()
    return (avg, str(int(br[0] / 10)))   # podeljeno sa brojem pitanja ???



def get_has_answers_subject(id):
    query = "SELECT * FROM odgovor_predmet " \
            "WHERE odgovor_predmet.id_semestra = %s AND odgovor_predmet.id_predmeta = %s"
    cursor.execute(query,(trenutni_semestar,id))
    cursor.fetchall()
    return cursor.rowcount > 0

def get_subject_primedbe(id):
    query = "SELECT p.odgovor, pi.tekst FROM odgovor_predmet p,pitanje pi WHERE pi.tip='predmet' "\
            "AND pi.format='tekst' AND p.id_pitanja=pi.id_pitanja "\
            "AND p.id_semestra = %s AND p.id_predmeta = %s"
    cursor.execute(query,(trenutni_semestar,id))
    rez = dict()
    for (odgovor, tekst) in cursor:
        if tekst not in rez:
            rez[tekst] = [odgovor]
        else:
            rez[tekst].append(odgovor)
    return rez


def get_techer_question_report(id_predmeta,id_nastavnika):
    query = "SELECT id_pitanja, tekst FROM pitanje WHERE tip='nastavnik' AND format='ocena' and id_pitanja>="+pitanja_min
    cursor.execute(query)
    pitanja = []
    for (id_pitanja, tekst) in cursor:
        pitanja.append((id_pitanja, tekst))
    izvestaj_global = {}
    for (id_pitanja, tekst) in pitanja:
        izvestaj = dict()
        # prosecna ocena
        query = "SELECT AVG(odgovor) FROM odgovor_nastavnik odg, drzi_predmet dp " \
                "WHERE odg.id_drzi_predmet = dp.id AND dp.id_nastavnika = %s AND dp.id_predmeta = %s "\
                "AND dp.id_semestra = %s AND odg.id_pitanja = %s  AND odgovor in (1,2,3,4,5)"
        cursor.execute(query, (id_nastavnika, id_predmeta,trenutni_semestar, id_pitanja))
        for (avg,) in cursor:
            izvestaj['prosecna_ocena'] = avg

        opcije = ['1', '2', '3', '4', '5', 'x']
        broj_glasova = dict.fromkeys(opcije, 0)
        for opcija in opcije:
            query = "SELECT COUNT(*) FROM odgovor_nastavnik odg, drzi_predmet dp " \
                    "WHERE odg.id_drzi_predmet = dp.id AND dp.id_nastavnika = %s AND dp.id_predmeta = %s "\
                    "AND odg.id_semestra = %s " \
                    "AND odg.id_pitanja = %s AND odg.odgovor = %s "
            cursor.execute(query, (id_nastavnika, id_predmeta, trenutni_semestar, id_pitanja, opcija))
            for (count,) in cursor:
                broj_glasova[opcija] = count
        suma = sum(broj_glasova.values())

        for opcija in opcije:
            izvestaj[opcija] = {"broj_glasova": broj_glasova[opcija],
                                    "procenat": ((int)(broj_glasova[opcija] * 100 / float(suma)))}
            izvestaj["ukupno"] = sum(broj_glasova.values())
            izvestaj_global[tekst] = izvestaj
    return izvestaj_global


def get_option_questions_teacher(id_predmeta, id_nastavnika):
    # pitanja sa ponudjenim opcijama
    izvestaj_global = {}

    query = "SELECT id_pitanja, tekst, format FROM pitanje WHERE tip ='nastavnik' AND format not like 'ocena' AND format not like 'tekst' AND id_pitanja>="+pitanja_min
    cursor.execute(query)
    pitanja = []
    for (id_pitanja, tekst, format) in cursor:
        pitanja.append((id_pitanja, tekst, format))
    for (id_pitanja, tekst, format) in pitanja:
        izvestaj = dict()
        opcije = format.split('|')
        broj_glasova = dict.fromkeys(opcije, 0)
        for opcija in opcije:
            query = "SELECT COUNT(*) FROM odgovor_nastavnik odg, drzi_predmet dp " \
                    "WHERE odg.id_drzi_predmet = dp.id AND dp.id_nastavnika = %s AND dp.id_predmeta = %s "\
                    "AND odg.id_semestra = %s " \
                    "AND odg.id_pitanja = %s AND odg.odgovor = %s "
            cursor.execute(query, (id_nastavnika, id_predmeta, trenutni_semestar, id_pitanja, opcija))
            for (count,) in cursor:
                broj_glasova[opcija] = count
        suma = sum(broj_glasova.values())

        for opcija in opcije:
            izvestaj[opcija] = {"broj_glasova": broj_glasova[opcija],
                                "procenat": (int)(broj_glasova[opcija] * 100 / float(suma))}
            izvestaj["ukupno"] = sum(broj_glasova.values())
            izvestaj_global[tekst] = izvestaj

    return izvestaj_global


def get_teachers_for_subject(id_predmeta):
    query = "SELECT n.ime, n.prezime, n.email, n.tip, n.id_nastavnika FROM nastavnik n, drzi_predmet dp " \
            "WHERE n.id_nastavnika=dp.id_nastavnika AND dp.id_predmeta = %s AND dp.id_semestra = %s GROUP BY n.id_nastavnika,n.tip"
    cursor.execute(query, (id_predmeta, trenutni_semestar))
    ret_val = []
    for (ime,prezime,email,tip,id) in cursor:
        ret_val.append((ime,prezime,email,tip,id))
    return ret_val

def get_has_answers_teacher(id_predmeta,id_nastavnika):
    query = "SELECT odgovor FROM odgovor_nastavnik,drzi_predmet " \
            "WHERE odgovor_nastavnik.id_semestra = %s AND odgovor_nastavnik.id_drzi_predmet = drzi_predmet.id " \
            "AND drzi_predmet.id_nastavnika = %s AND drzi_predmet.id_predmeta = %s "
    cursor.execute(query,(trenutni_semestar,id_nastavnika,id_predmeta))
    cursor.fetchall()
    return cursor.rowcount > 0

def get_teacher_primedbe(id_predmeta, id_nastavnika):
    query = "SELECT odgovor_nastavnik.odgovor, p.tekst FROM odgovor_nastavnik,pitanje p, drzi_predmet WHERE p.tip='nastavnik' "\
            "AND p.format='tekst' AND odgovor_nastavnik.id_pitanja=p.id_pitanja "\
            "AND odgovor_nastavnik.id_semestra = %s AND odgovor_nastavnik.id_drzi_predmet = drzi_predmet.id " \
            "AND drzi_predmet.id_nastavnika = %s AND drzi_predmet.id_predmeta = %s "
    cursor.execute(query,(trenutni_semestar,id_nastavnika,id_predmeta))
    rez = dict()
    for (odgovor, tekst) in cursor:
        if tekst not in rez:
            rez[tekst] = [odgovor]
        else:
            rez[tekst].append(odgovor)
    return rez


# da li se predmet drzao u trenutnom semestru
def subject_was_in_current_semester(id):
    query = "SELECT * FROM drzi_predmet WHERE id_predmeta = %s and id_semestra = %s"
    cursor.execute(query, (id,trenutni_semestar,))
    cursor.fetchall()
    return cursor.rowcount > 0


def get_subject_answer_counts(id):
    opcije = ['1', '2', '3', '4', '5', 'x']
    broj_glasova = dict.fromkeys(opcije, 0)
    for opcija in opcije:
        query = "SELECT COUNT(*) FROM odgovor_predmet " \
                "WHERE odgovor_predmet.id_semestra = %s " \
                "AND id_pitanja = %s AND odgovor_predmet.odgovor = %s " \
                "AND id_predmeta = %s"
        cursor.execute(query, (trenutni_semestar, pitanje_id_predmet, opcija,id))
        for (count,) in cursor:
            broj_glasova[opcija] = count
    suma = sum(broj_glasova.values())
    return suma

def get_subject_teacher_answer_counts(id_nastavnika, id_predmeta):
    opcije = ['1', '2', '3', '4', '5', 'x']
    broj_glasova = dict.fromkeys(opcije, 0)
    for opcija in opcije:
        query = "SELECT COUNT(*) FROM odgovor_nastavnik odg, drzi_predmet dp " \
                "WHERE odg.id_drzi_predmet = dp.id AND dp.id_nastavnika = %s AND dp.id_predmeta = %s " \
                "AND odg.id_semestra = %s " \
                "AND odg.id_pitanja = %s AND odg.odgovor = %s "
        cursor.execute(query, (id_nastavnika, id_predmeta, trenutni_semestar, pitanje_id_nastavnik, opcija))
        for (count,) in cursor:
            broj_glasova[opcija] = count
    suma = sum(broj_glasova.values())
    return suma

def get_techers_total_avg():
    query = "SELECT AVG(odgovor) FROM odgovor_nastavnik odg " \
             "WHERE odg.id_semestra = %s  AND odg.odgovor in (1,2,3,4,5)"
    cursor.execute(query, (trenutni_semestar,))
    avg = "{0:.2f}".format(cursor.fetchone()[0])
    return avg

def get_subjects_total_avg():
    query = "SELECT AVG(odgovor) FROM odgovor_predmet odg " \
             "WHERE odg.id_semestra = %s  AND odg.odgovor in (1,2,3,4,5)"
    cursor.execute(query, (trenutni_semestar,))
    avg = "{0:.2f}".format(cursor.fetchone()[0])
    return avg