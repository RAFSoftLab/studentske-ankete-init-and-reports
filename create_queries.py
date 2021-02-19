# -*- coding: utf-8 -*-

# nema referencijalnih integriteta, mora programski da se proverava

TABLES = dict()
TABLES['semestar'] = ("CREATE TABLE `semestar` (\
 `id_semestra` int(11) NOT NULL AUTO_INCREMENT,\
 `skolska_godina` varchar(10) COLLATE utf8_unicode_ci NOT NULL,\
 `tip_semestra` varchar(10) COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_semestra`)\
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ROW_FORMAT=COMPACT")

TABLES['student'] = ("CREATE TABLE `student` (\
 `id_studenta` int(11) NOT NULL AUTO_INCREMENT,\
 `username` varchar(80) NOT NULL,\
 `ime` varchar(50) COLLATE utf8_unicode_ci NOT NULL,\
 `prezime` varchar(50) COLLATE utf8_unicode_ci NOT NULL,\
 `smer` varchar(20) COLLATE utf8_unicode_ci,\
 `indeks` varchar(20) COLLATE utf8_unicode_ci,\
 `godinaUpisa` varchar(20) COLLATE utf8_unicode_ci,\
 PRIMARY KEY (`id_studenta`)\
)ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['studentski_nalog'] = ("CREATE TABLE `studentski_nalog` (\
 `id` int(11) NOT NULL AUTO_INCREMENT,\
 `id_studenta` int(11) NOT NULL,\
 `username` varchar(40) COLLATE utf8_unicode_ci NOT NULL,\
 `password` varchar(40) COLLATE utf8_unicode_ci NOT NULL,\
 `email` varchar(50) COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id`)\
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['predmet'] = ("CREATE TABLE `predmet` (\
 `id_predmeta` int(11) NOT NULL AUTO_INCREMENT,\
 `naziv` varchar(60) COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_predmeta`),\
 UNIQUE KEY `naziv` (`naziv`)\
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['nastavnik'] = ("CREATE TABLE `nastavnik` (\
 `id_nastavnika` int(11) NOT NULL AUTO_INCREMENT,\
 `ime` varchar(40) COLLATE utf8_unicode_ci NOT NULL,\
 `prezime` varchar(40) COLLATE utf8_unicode_ci NOT NULL,\
 `tip` varchar(20) COLLATE utf8_unicode_ci NOT NULL,\
 `email` varchar(40) COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_nastavnika`),\
 UNIQUE KEY `ime` (`ime`,`prezime`,`tip`)\
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['drzi_predmet'] = ("CREATE TABLE `drzi_predmet` (\
 `id` int(11) NOT NULL AUTO_INCREMENT,\
 `id_nastavnika` int(11) NOT NULL,\
 `id_predmeta` int(11) NOT NULL,\
 `grupa` varchar(10) NOT NULL,\
 `id_semestra` int(11) NOT NULL,\
 PRIMARY KEY (`id`),\
 UNIQUE KEY `id_nastavnika` (`id_nastavnika`,`id_predmeta`,`grupa`,`id_semestra`)\
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['pitanje'] = ("CREATE TABLE `pitanje` (\
 `id_pitanja` int(11) NOT NULL AUTO_INCREMENT,\
 `tekst` text COLLATE utf8_unicode_ci NOT NULL,\
 `tip` varchar(20) COLLATE utf8_unicode_ci NOT NULL,\
 `format` varchar(100) COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_pitanja`)\
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['odgovor_fakultet'] = ("CREATE TABLE `odgovor_fakultet` (\
 `id_odgovora` int(11) NOT NULL AUTO_INCREMENT,\
 `id_pitanja` int(11) NOT NULL,\
 `id_studenta` int(11),\
 `id_semestra` int(11) NOT NULL,\
 `odgovor` text COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_odgovora`),\
 UNIQUE KEY `id_pitanja` (`id_pitanja`,`id_studenta`,`id_semestra`)\
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['odgovor_predmet'] = ("CREATE TABLE `odgovor_predmet` (\
 `id_odgovora` int(11) NOT NULL AUTO_INCREMENT,\
 `id_pitanja` int(11) NOT NULL,\
 `id_studenta` int(11),\
 `id_predmeta` int(11) NOT NULL,\
 `id_semestra` int(11) NOT NULL,\
 `odgovor` text COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_odgovora`),\
 UNIQUE KEY `id_pitanja_2` (`id_pitanja`,`id_studenta`,`id_predmeta`,`id_semestra`)\
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['odgovor_nastavnik'] = ("CREATE TABLE `odgovor_nastavnik` (\
 `id_odgovora` int(11) NOT NULL AUTO_INCREMENT,\
 `id_pitanja` int(11) NOT NULL,\
 `id_studenta` int(11),\
 `id_drzi_predmet` int(11) NOT NULL,\
 `id_semestra` int(11) NOT NULL,\
 `odgovor` text COLLATE utf8_unicode_ci NOT NULL,\
 PRIMARY KEY (`id_odgovora`),\
 UNIQUE KEY `id_pitanja_2` (`id_pitanja`,`id_studenta`,`id_drzi_predmet`,`id_semestra`)\
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ROW_FORMAT=COMPACT")


TABLES['zakljucena'] = ("CREATE TABLE `zakljucena` (\
 `id_studenta` int(11)  NOT NULL,\
 `id_semestra` int(11) NOT NULL\
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")

TABLES['student_predmet_semestar'] = ("CREATE TABLE `student_predmet_semestar` (\
 `id_semestra` int(11) NOT NULL,\
 `id_studenta` int(11)  NOT NULL,\
 `id_predmeta` int(11) NOT NULL\
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci")