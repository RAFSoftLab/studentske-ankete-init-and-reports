import report_queries as rq
import codecs

file_path = "output20202021-neparni/public/"
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

        primedbe = rq.get_faculty_primedbe()
        for tekst in primedbe.keys():
            fajl.write("<br><h3>" + tekst + "</h3>")
            for p in primedbe[tekst]:
                if (p):
                    fajl.write(p)
                    fajl.write("<br>-----------------------------------------------------------------<br>")
        fajl.write("</body>")
        fajl.write("</html>")


def subject_reports_for_teachers():
    predmeti = rq.get_all_subjects()
    ret_val = [] # vracamo listu torki oblika (predmet,email_nastavnika, lista html fajlova, id_predmeta)
    for p in predmeti.keys():
        if not rq.subject_was_in_current_semester(predmeti[p]):
            continue;
        naziv_fajla = file_path+str(p).replace(" ","_")+".php"
        naziv_za_link = str(p).replace(" ","_")+".php"
        with codecs.open(naziv_fajla, "w+", "utf-8") as fajl:
            fajl.write(login_path_php)
            fajl.write("<html>")
            fajl.write("<head><meta charset='UTF-8'></meta></head>")
            fajl.write("<body style='letter-spacing:1px';'font-family:Arial'>")
            fajl.write("<h2>Rezultati studentske ankete za " + text_sem+ " godine</h2><br>")
            fajl.write("<a href=index.php>Povratak</a><br>")
            index.write("&nbsp;&nbsp;&nbsp;<a href=" + naziv_za_link + ">"+p+"</a><br><br>")
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

    return ret_val

if __name__ == "__main__":
    with codecs.open(index_path, "w+", "utf-8") as index:
        index.write(login_path_php)
        index.write("<html>")
        index.write("<head><meta charset='UTF-8'></meta></head>")
        index.write("<body style='letter-spacing:1px';'font-family:Arial'>")
        index.write("<h2>Računarski fakultet</h2><h2>Rezultati studentske ankete za "+text_sem+" godine</h2><br>")
        faculty_reports()
        index.write("<h3>Predmeti</h3><br>")
        subject_reports_for_teachers()
        index.write("</body>")
        index.write("</html>")