import report_queries as rq
import codecs

#from studsluzba_import import broj

file_path = "output20202021-neparni/public-min/"
index_path = file_path+"index.php"
text_sem = 'neparni semestar školske 2020/2021.'
login_path_php = '<?php require_once __DIR__ . \'/../login/izvestajneparni20202021.php\';  ?>'

from report import opcije

def faculty_reports():
    naziv_fajla = file_path + "izvestaj_fakultet.php"
    naziv_za_link = "izvestaj_fakultet.php"
    index.write("<a href="+naziv_za_link+">Opšta pitanja</a><br><br>")
    with codecs.open(naziv_fajla, "w+", "utf-8") as fajl:
        fajl.write(login_path_php)
        fajl.write("<html>")
        fajl.write("<head><meta charset='UTF-8'></meta></head>")
        fajl.write("<body style='letter-spacing:1px';'font-family:Arial'>")
        fajl.write("<h2>Rezultati studentske ankete za "+text_sem + " godine - opšta pitanja</h2><br><br>")
        fajl.write("<a href=index.php>Povratak</a><br>")
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
        fajl.write("</body>")
        fajl.write("</html>")


def subject_reports_for_teachers():
    predmeti = rq.get_all_subjects()
    ret_val = [] # vracamo listu torki oblika (predmet,email_nastavnika, lista html fajlova, id_predmeta)
    avg_nastavnik = rq.get_techers_total_avg()
    avg_predmet = rq.get_subjects_total_avg()
    index.write("<br>Ukupna prosečna ocena svih predmeta: <b>" + str(avg_predmet) + "</b><br>")
    index.write("<br>Ukupna prosečna ocena svih nastavnika i saradnika: <b>"+str(avg_nastavnik)+"</b><br>")
    index.write("<br><br>Prosečne ocene za predmete, nastavnike i saradnike<br><br>")
    index.write("<table border=1");
    index.write("<thead><td style=\"background-color: #eee;\">Predmet [Nastavnik]</td><td style=\"background-color: #eee;\">Prosečna ocena</td><td style=\"background-color: #eee;\">Broj studenata</td></thead>")
    for p in predmeti.keys():
        if not rq.subject_was_in_current_semester(predmeti[p]):
            continue;
        if rq.get_has_answers_subject(predmeti[p]):
            avg = rq.get_subject_avg(predmeti[p])
            index.write("<tr><td >"+ p + "</td>")
            index.write("<td>"+avg[0] + "</td>")  # if ocene['prosecna_ocena'] is None:
            broj_odgovora = rq.get_subject_answer_counts(predmeti[p])
            index.write("<td>" + str(broj_odgovora) + "</td></tr>")
            teachers = rq.get_teachers_for_subject(predmeti[p])  # (ime,prezime,email,tip,id)
            for t in teachers:
                index.write("<tr><td>" + p+ "-" + t[3] + " " + t[0] + " " + t[1] + "</td>")
                if rq.get_has_answers_teacher(predmeti[p], t[4]):
                    avg_prof = rq.get_teacher_avg(t[4], predmeti[p])
                    index.write("<td>" + avg_prof[0] + "</td>")
                    broj_odgovora_nastavnik = rq.get_subject_teacher_answer_counts(t[4],predmeti[p])
                    index.write("<td>"+str(broj_odgovora_nastavnik)+ "</td><tr>")
    index.write("</table>")


with codecs.open(index_path, "w+", "utf-8") as index:
    index.write(login_path_php)
    index.write("<html>")
    index.write("<head><meta charset='UTF-8'></meta></head>")
    index.write("<body style='letter-spacing:1px';'font-family:Arial'>")
    index.write("<h2>Računarski fakultet</h2><h2>Rezultati studentske ankete za "+text_sem+" godine</h2><br>")
    faculty_reports()
    subject_reports_for_teachers()
    index.write("</body>")
    index.write("</html>")