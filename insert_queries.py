# -*- coding: utf-8 -*-`

INSERTS = {}


INSERTS['nastavnik'] = ("INSERT INTO nastavnik "
                        "(ime, prezime, tip, email) "
                        "VALUES (%s, %s, %s, %s)")

INSERTS['predmet'] = ("INSERT INTO predmet "
                      "(naziv) "
                      "VALUES (%s)")

INSERTS['predmetsifra'] = ("INSERT INTO predmet "
                      "(sifra, naziv) "
                      "VALUES (%s, %s)")


INSERTS['drzi_predmet'] =("INSERT INTO drzi_predmet "
                          "(id_nastavnika, id_predmeta, grupa, id_semestra) "
                          "VALUES (%s, %s, %s, %s)")

INSERTS['pitanje'] = ("INSERT INTO pitanje "
                      "(tekst, tip, format) "
                      "VALUES (%s, %s, %s)")


INSERTS['semestar'] = ("INSERT INTO `semestar` (`skolska_godina`, `tip_semestra`) VALUES "
                                "(%s, %s)")



INSERTS['student'] = ("INSERT INTO `student` (`ime`, `prezime`, `smer`, `indeks`, `godinaUpisa`, `username` ) VALUES"
                      "(%s, %s, %s, %s, %s,  %s)")

INSERTS['student1'] = ("INSERT INTO `student` (`ime`, `prezime`, `smer`, `indeks`, `godinaUpisa`, `username`, `usernamestari`  ) VALUES"
                      "(%s, %s, %s, %s, %s,  %s, %s)")



INSERTS['studentski_nalog'] = ("INSERT INTO `studentski_nalog` (`id_studenta`, `username`, `password`) VALUES"
                               "(1, 'ivan', 'ivan'),"
                               "(2, 'marko', 'marko'),"
                               "(3, 'nikola', 'nikola');")



INSERTS['student_predmet_semestar'] = ("INSERT INTO `student_predmet_semestar` "
                                       "(`student_id`, `predmet_id`,`semestar_id` ) VALUES  (%s, %s, %s)")
