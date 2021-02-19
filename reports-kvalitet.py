import report_queries as rq
import codecs
import pdfkit





file_path = "output/kvalitet/"
index_path = file_path+"izvestaj_kvalitet.html"



def faculty_reports():   
        index.write("<h3>Opšta pitanja</h3>")
        pitanja = rq.get_faculty_questions_reports()
        for tekst_pitanja, ocene in pitanja.items():
            index.write(tekst_pitanja + "<br><br>")
            index.write("Prosečna ocena: " + str(round(ocene['prosecna_ocena'], 2)) + "<br>")
            index.write("Ukupno glasalo: " + str(ocene['ukupno']) + "<br>")
            for ocena in range(1, 6):
                index.write("\t" + str(ocena) + ": ")
                index.write(str(ocene[ocena]['broj_glasova']) + " glasova ")
                index.write("(" + str(ocene[ocena]['procenat']) + "%)<br>")
            index.write("<br><br>")
        primedbe = rq.get_faculty_primedbe()
        index.write("<br><h3>Primedbe/zamerke:</h3>")
        for p in primedbe:
            if (p):
                index.write(p)
                index.write("<br>-----------------------------------------------------------------<br>")


def subject_reports_for_teachers():
    predmeti = rq.get_all_subjects()
    for p in predmeti.keys():
            index.write("<h3>Predmet: "+p+"</h3>")
            if rq.get_has_answers_subject(predmeti[p]):
                index.write("Prosečna ocene za predmet: ")
                avg = rq.get_subject_avg(predmeti[p])
                index.write(avg[0] + " ("+avg[1]+")")
                index.write("<br>")
            else:
                index.write("Nema odgovora")
            teachers = rq.get_teachers_for_subject(predmeti[p])
            for t in teachers:
                if rq.get_has_answers_teacher(predmeti[p],t[4]):
                   index.write(t[0]+" " +t[1]+ " (" + t[3] + ")" + ":  ")
                   avg_prof = rq.get_teacher_avg(t[4],predmeti[p])
                   index.write(avg_prof[0] + " ("+avg_prof[1]+")")
                   index.write("<br>")





with codecs.open(index_path, "w+", "utf-8") as index:
    index.write("<html>")
    index.write("<head><meta charset='UTF-8'></meta></head>")
    index.write("<body style='letter-spacing:1px';'font-family:Arial'>")
    index.write("<h2>Računarski fakultet</h2><h2>Rezultati studentske ankete za parni semestar školske 2017/2018. godine</h2><br>")
    faculty_reports()
    index.write("<br><h2>Prosečne ocene za predmete i nastavnike</h2><br>")
    subject_reports_for_teachers()
    index.write("</body>")
    index.write("</html>")
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8"
    }

    pdfkit.from_file(index_path, file_path+"izvestaj-ankete-parni201718.pdf", options)