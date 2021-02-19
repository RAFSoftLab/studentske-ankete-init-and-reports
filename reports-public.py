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
            fajl.write("<h3>Predmet: "+p+"</h3>")
            index.write("<br><h3>"+p+"</h3>")
            index.write("&nbsp;&nbsp;&nbsp;<a href=" + naziv_za_link + ">Predmet</a><br><br>")
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
                teachers = rq.get_teachers_for_subject(predmeti[p])  # (ime,prezime,email,tip,id)
                for t in teachers:
                    naziv_fajla_prof = file_path + str(p).replace(" ", "_") + "-" + t[0] + str(t[1]).replace(" ", "") + \
                                       t[3] + ".php"
                    with codecs.open(naziv_fajla_prof, "w+", "utf-8") as fajl_prof:
                        fajl_prof.write(login_path_php)
                        fajl_prof.write("<html>")
                        fajl_prof.write("<head><meta charset='UTF-8'></meta></head>")
                        fajl_prof.write("<body style='letter-spacing:1px';'font-family:Arial'>")
                        fajl_prof.write("<h2>Rezultati ankete za " + text_sem + " godine</h2><br>")
                        fajl_prof.write("<h3>" + t[3] + " " + t[0] + " " + t[1] + " na predmetu " + p + "</h3>")
                        naziv_za_link = str(p).replace(" ", "_") + "-" + t[0] + str(t[1]).replace(" ", "") + t[3] + ".php"
                        index.write("&nbsp;&nbsp;&nbsp;<a href=" + naziv_za_link + ">"+t[0]+" "+t[1]+" "+t[3]+"</a><br><br>")
                        fajl_prof.write("<a href=index.php>Povratak</a><br>")
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
    return ret_val

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