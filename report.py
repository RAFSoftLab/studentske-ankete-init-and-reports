# -*- coding: utf-8 -*-
import report_queries as rq
import codecs
import pdfkit
# from databaseconfig import *
from gmailclient import *

file_path = "output20202021-neparni/"
file_path_rep = "reports20202021-neparni"
file_path_pdf = "output20202021-neparni/pdf/"
profesori_emails = set()
opcije = ['1', '2', '3', '4', '5', 'x']

text_sem = 'neparni semestar školske 2020/2021.'


def faculty_reports():
    naziv_fajla = file_path + "izvestaj_fakultet.html"
    with codecs.open(naziv_fajla, "w+", "utf-8") as fajl:
        fajl.write("<html>")
        fajl.write("<head><meta charset='UTF-8'></meta></head>")
        fajl.write("<body style='letter-spacing:1px';'font-family:Arial'>")
        fajl.write("<h2>Rezultati ankete za " + text_sem + " godine - opšta pitanja</h2><br><br>")
        fajl.write("<h3>Statistika pitanja:</h3>")
        pitanja = rq.get_faculty_questions_reports()
        for tekst_pitanja, ocene in pitanja.items():
            fajl.write(tekst_pitanja + "<br><br>")
            fajl.write("Prosečna ocena: " + str(round(ocene['prosecna_ocena'], 2)) + "<br>")
            fajl.write("Ukupno glasalo: " + str(ocene['ukupno']) + "<br>")
            for ocena in opcije:
                fajl.write("\t" + str(ocena) + ": ")
                fajl.write(str(ocene[ocena]['broj_glasova']) + " glasova ")
                fajl.write("(" + str(ocene[ocena]['procenat']) + "%)<br>")
            fajl.write("<br><br>")
        # pitanja sa opcijama
        pitanja = rq.get_option_questions_fakultet()

        for tekst_pitanja, odgovori in pitanja.items():
            fajl.write(tekst_pitanja + "<br><br>")
            fajl.write("Ukupno glasalo: " + str(odgovori['ukupno']) + "<br><br>")
            fajl.write('<table border=1>')
            fajl.write('<tr><td>Opcija</td><td>Broj glasova</td><td>Procenat</td></tr>')
            for opcija in odgovori.keys():
                fajl.write('<tr>')
                if opcija != 'ukupno':
                    fajl.write('<td>' + opcija + '</td>')
                    fajl.write('<td>' + str(odgovori[opcija]['broj_glasova']) + "</td>")
                    fajl.write("<td>" + str(odgovori[opcija]['procenat']) + "%</td>")
                fajl.write('</tr>')
            fajl.write('</table>')
            fajl.write("<br><br>")

        primedbe = rq.get_faculty_primedbe()
        for tekst in primedbe.keys():
            fajl.write("<br><h3>" + tekst + "</h3>")
            for p in primedbe[tekst]:
                if (p):
                    fajl.write(p)
                    fajl.write("<br>-----------------------------------------------------------------<br>")
        fajl.write("</body>")
        fajl.write("</html>")


# pdf fajlovi za profesore
def subject_reports_for_teachers():
    predmeti = rq.get_all_subjects()
    ret_val = []  # vracamo listu torki oblika (predmet,email_nastavnika, lista html fajlova, id_predmeta)
    for p in predmeti.keys():
        if not rq.subject_was_in_current_semester(predmeti[p]):
            continue;
        naziv_fajla = file_path + str(p).replace(" ", "_") + ".html"
        with codecs.open(naziv_fajla, "w+", "utf-8") as fajl:
            fajl.write("<html>")
            fajl.write("<head><meta charset='UTF-8'></meta></head>")
            fajl.write("<body style='letter-spacing:1px';'font-family:Arial'>")
            fajl.write("<h2>Rezultati ankete za " + text_sem + " godine za predmet</h2><br>")
            fajl.write("<h3>Predmet: " + p + "</h3><br>")

            if rq.get_has_answers_subject(predmeti[p]):
                avg = rq.get_subject_avg(predmeti[p])
                fajl.write("<h3>Ukupna prosečna ocena: " + avg[0] + "</h3><br>")
                fajl.write("<h3>Prosečne ocene po pitanjima</h3><br>")
                pitanja = rq.get_subject_question_report(predmeti[p])
                for tekst_pitanja, ocene in pitanja.items():
                    fajl.write(tekst_pitanja + "<br><br>")
                    if ocene['prosecna_ocena'] is None:
                        prosecna_ocena = "nema ocena"
                    else:
                        prosecna_ocena = str(round(ocene['prosecna_ocena'], 2))
                    fajl.write("Prosečna ocena: " + prosecna_ocena + "<br>")
                    fajl.write("Ukupno glasalo: " + str(ocene['ukupno']) + "<br>")
                    for ocena in opcije:
                        fajl.write("\t" + str(ocena) + ": ")
                        fajl.write(str(ocene[ocena]['broj_glasova']) + " glasova ")
                        fajl.write("(" + str(ocene[ocena]['procenat']) + "%)<br>")
                    fajl.write("<br><br>")
                pitanja = rq.get_option_questions_subject(predmeti[p])
                for tekst_pitanja, odgovori in pitanja.items():
                    fajl.write(tekst_pitanja + "<br><br>")
                    fajl.write("Ukupno glasalo: " + str(odgovori['ukupno']) + "<br><br>")
                    fajl.write('<table border=1>')
                    fajl.write('<tr><td>Opcija</td><td>Broj glasova</td><td>Procenat</td></tr>')
                    for opcija in odgovori.keys():
                        fajl.write('<tr>')
                        if opcija != 'ukupno':
                            fajl.write('<td>' + opcija + '</td>')
                            fajl.write('<td>' + str(odgovori[opcija]['broj_glasova']) + "</td>")
                            fajl.write("<td>" + str(odgovori[opcija]['procenat']) + "%</td>")
                        fajl.write('</tr>')
                    fajl.write('</table>')
                    fajl.write("<br><br>")
                primedbe = rq.get_subject_primedbe(predmeti[p])
                for tekst in primedbe.keys():
                    fajl.write("<br><h3>" + tekst + "</h3>")
                    for pr in primedbe[tekst]:
                        if (pr):
                            fajl.write(pr)
                            fajl.write("<br>-----------------------------------------------------------------<br>")

            else:
                fajl.write("Nema odgovora")

            teachers = rq.get_teachers_for_subject(predmeti[p])  # (ime,prezime,email,tip,id)
            for t in teachers:
                naziv_fajla_prof = file_path + str(p).replace(" ", "_") + "-" + t[0] + str(t[1]).replace(" ", "") + t[
                    3] + ".html"
                with codecs.open(naziv_fajla_prof, "w+", "utf-8") as fajl_prof:
                    fajl_prof.write("<html>")
                    fajl_prof.write("<head><meta charset='UTF-8'></meta></head>")
                    fajl_prof.write("<body style='letter-spacing:1px';'font-family:Arial'>")
                    fajl_prof.write("<h2>Rezultati ankete za " + text_sem + " godine za nastavnika</h2><br>")
                    fajl_prof.write("<h3>" + t[3] + " " + t[0] + " " + t[1] + " na predmetu " + p + "</h3>")
                    if rq.get_has_answers_teacher(predmeti[p], t[4]):
                        ocene = rq.get_techer_question_report(predmeti[p], t[4])
                        avg_prof = rq.get_teacher_avg(t[4], predmeti[p])
                        fajl_prof.write("<br><h3>Ukupna prosečna ocena: " + avg_prof[0] + "</h3><br>")
                        fajl_prof.write("<h3>Prosečne ocene po pitanjima</h3>")
                        for tekst_pitanja, ocene in ocene.items():
                            fajl_prof.write("<br>" + tekst_pitanja + "<br><br>")
                            if ocene['prosecna_ocena'] is None:
                                prosecna_ocena = "nema ocena"
                            else:
                                prosecna_ocena = str(round(ocene['prosecna_ocena'], 2))
                            fajl_prof.write("Prosečna ocena: " + prosecna_ocena + "<br>")
                            fajl_prof.write("Ukupno glasalo: " + str(ocene['ukupno']) + "<br>")
                            for ocena in opcije:
                                fajl_prof.write("\t" + str(ocena) + ": ")
                                fajl_prof.write(str(ocene[ocena]['broj_glasova']) + " glasova ")
                                fajl_prof.write("(" + str(ocene[ocena]['procenat']) + "%)<br>")
                        pitanja = rq.get_option_questions_teacher(predmeti[p], t[4])
                        for tekst_pitanja, odgovori in pitanja.items():
                            fajl.write(tekst_pitanja + "<br><br>")
                            fajl.write("Ukupno glasalo: " + str(odgovori['ukupno']) + "<br><br>")
                            fajl.write('<table border=1>')
                            fajl.write('<tr><td>Opcija</td><td>Broj glasova</td><td>Procenat</td></tr>')
                            for opcija in odgovori.keys():
                                fajl.write('<tr>')
                                if opcija != 'ukupno':
                                    fajl.write('<td>' + opcija + '</td>')
                                    fajl.write('<td>' + str(odgovori[opcija]['broj_glasova']) + "</td>")
                                    fajl.write("<td>" + str(odgovori[opcija]['procenat']) + "%</td>")
                                fajl.write('</tr>')
                            fajl.write('</table>')
                            fajl.write("<br><br>")

                        primedbe_t = rq.get_teacher_primedbe(predmeti[p], t[4])
                        for tekst in primedbe_t.keys():
                            fajl_prof.write("<br><h3>" + tekst + "</h3>")
                            for pr in primedbe_t[tekst]:
                                if (pr):
                                    fajl_prof.write(pr)
                                    fajl_prof.write(
                                        "<br>-----------------------------------------------------------------<br>")
                        fajl_prof.write("<br><br>")
                        fajl_prof.write("</body>")
                        fajl_prof.write("</html>")
                    else:
                        fajl_prof.write("Nema odgovora")
                # t - # (ime,prezime,email,tip,id)
                if t[3] == 'Profesor':
                    profesori_emails.add(t[2])
                    ret_val.append((p, t[3], t[2], [naziv_fajla, naziv_fajla_prof], predmeti[p]))
                if t[3] == 'Asistent' or t[3] == 'Saradnik':
                    ret_val.append((p, t[3], t[2], [naziv_fajla_prof], predmeti[p]))

            for it in ret_val:  # (id predmeta, tipnastavnika, email, fajlovi, naziv predmeta)
                # if rq.get_has_answers_subject(it[0]):
                if it[1] == 'Asistent' or it[1] == 'Saradnik':
                    p = it[0]
                    for its in ret_val:
                        if its[1] == 'Profesor' and p == its[
                            0]:  # isti predmeti  #str(its[0]).replace(" ","_") == str(p).replace(" ","_"):
                            for item in it[3]:
                                if not item in its[3]:
                                    its[3].append(item)
            fajl.write("</body>")
            fajl.write("</html>")
    return ret_val


# html izvestaj za studente - bez komenatara, samo ocene

def subject_reports_for_students():
    predmeti = rq.get_all_subjects()
    for p in predmeti.keys():
        naziv_fajla = file_path_rep + "studenti" + "/" + str(p).replace(" ", "_") + ".html"
        naziv_fajla_index = file_path_rep + "_stud" + "/index.html"
        with codecs.open(naziv_fajla, "w+", "utf-8") as fajl:
            fajl.write("<html>")
            fajl.write("<head><meta charset='UTF-8'></meta></head>")
            fajl.write("<body style='letter-spacing:1px';'font-family:Arial'>")
            fajl_prof.write("<h2>Rezultati ankete za " + text_sem + " godine</h2><br>")
            fajl.write("<h3>Predmet: " + p + "</h3><br>")
            fajl.write("<h3>Prosečne ocene za predmet</h3><br>")
            if rq.get_has_answers_subject(predmeti[p]):
                pitanja = rq.get_subject_question_report(predmeti[p])
                for tekst_pitanja, ocene in pitanja.items():
                    fajl.write(tekst_pitanja + "<br><br>")
                    fajl.write("Prosečna ocena: " + str(round(ocene['prosecna_ocena'], 2)) + "<br>")
                    for ocena in range(1, 6):
                        fajl.write("\t" + str(ocena) + ": ")
                        fajl.write(str(ocene[ocena]['broj_glasova']) + " glasova ")
                        fajl.write("(" + str(ocene[ocena]['procenat']) + "%)<br>")
                    fajl.write("<br><br>")
            else:
                fajl.write("Nema odgovora")
            teachers = rq.get_teachers_for_subject(predmeti[p])
            for t in teachers:
                if rq.get_has_answers_teacher(predmeti[p], t[4]):
                    ocene = rq.get_techer_question_report(predmeti[p], t[4])
                    naziv_fajla_prof = file_path_rep + "_stud" + "/" + str(p).replace(" ", "_") + "-" + t[0] + t[1] + t[
                        3] + ".html"
                    with codecs.open(naziv_fajla_prof, "w+", "utf-8") as fajl_prof:
                        fajl_prof.write("<html>")
                        fajl_prof.write("<body style='letter-spacing:1px';'font-family:Arial'>")
                        fajl_prof.write("<h2>Rezultati ankete za parni semestar školske 2017/2018. godine</h2><br>")
                        fajl_prof.write("<h3>" + t[3] + " " + t[0] + " " + t[1] + " na predmetu " + p + "</h3>")
                        fajl_prof.write("<h3>Prosečne ocene za nastavnika</h3><br>")
                        for tekst_pitanja, ocene in ocene.items():
                            fajl_prof.write("<br>" + tekst_pitanja + "<br><br>")
                            fajl_prof.write("Prosečna ocena: " + str(round(ocene['prosecna_ocena'], 2)) + "<br>")
                            for ocena in range(1, 6):
                                fajl_prof.write("\t" + str(ocena) + ": ")
                                fajl_prof.write(str(ocene[ocena]['broj_glasova']) + " glasova ")
                                fajl_prof.write("(" + str(ocene[ocena]['procenat']) + "%)<br>")
                        fajl_prof.write("</body>")
                        fajl_prof.write("</html>")

            fajl.write("</body>")
            fajl.write("</html>")


def create_pdf(html_files, naziv_fajla):
    config = pdfkit.configuration(wkhtmltopdf=r'/usr/bin/wkhtmltopdf')
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8"

    }
    ime = file_path_pdf + naziv_fajla + ".pdf"
    pdfkit.from_file(html_files, file_path_pdf + naziv_fajla + ".pdf", options, configuration=config)
    return ime


def send_reports():
    create_pdf([file_path + "izvestaj_fakultet.html"], "opsta_pitanja")

    za_pdf = subject_reports_for_teachers()
    za_slanje = dict()
    for item in za_pdf:
        ime_fajla = create_pdf(item[3], item[0] + "-" + item[1] + "-" + item[2][:-7])
        if za_slanje.get(item[2]):
            za_slanje.get(item[2]).append(ime_fajla)
        else:
            za_slanje[item[2]] = [ime_fajla]

    print(za_slanje)

    # test send email

    text = "Poštovane kolege,\n\nU atačmentu šaljemo obrađene rezultate Ankete o nastavi na Računarskom " \
           "fakultetu za " +text_sem+" godine za Vaše " \
           "predmete. U slučaju da imate bilo kakvih pitanja molimo Vas da se javite na email anketa@raf.rs.\n\nFakultet"

    create_and_send_message("anketa@raf.rs", "bdimicsurla@raf.rs",
                            "Rezultati studentske ankete-"+text_sem, text,
                            za_slanje["bdimicsurla@raf.rs"])

    # print(profesori_emails)
    #
    # for item, value in za_slanje.items():
    #     print(item)
    #     print(value)
    #     print('\n')
    #     create_and_send_message("anketa@raf.rs", item, "Rezultati studentske ankete-"+text_sem, text,
    #                             value)



if __name__ == "__main__":
    faculty_reports()


