
### Softver za pripremu podataka za anketiranje studenata o predmetima i nastavnicima, obradu podataka i generisanje raznih vrsta izveštaja

Veb aplikacija za anketiranje: https://github.com/RAFSoftLab/studentske-ankete-webapp


###Koraci u pripremi baze za anketiranje:

Prvo podizanje baze

1. Kreirati bazu na serveru (MySQL)

2. Upisati sve podatke potrebne za konekciju u `databaseconfig.py` u promenljivu `mysqlParams`

3. Pokrenuti skriptu  `database_init.py`, skripta pravi tabele i importuje pitanja za anketu

Priprema podataka za anketiranje za jedan semestar

4. Import podataka iz rasporeda (koji nastavnik drži koji predmet u semestru), zadaje se školska godina, semestar (z-zimski, l-letnji) i putanja do fajla sa rasporedom za semestar (csv fajl)

`python import_semester_data.py "2020/2021" z csv`

5. Posle izvršene skripte u prethodnom koraku na stdout se ispisuje dodeljeni id semestra za koji se priprema anketiranje, taj broj upisati ručno u `databaseconfig.py` u promenljivu `trenutni_semestar` 

6. Importovati podatke o studentima koji slušaju predmete, ovi podaci se u sadašnjoj verziji importuju iz mejl listi pomoću skripte `maillist_import.py`. Prosleđuju se dve url putanje, api za preuzimanje svih predmeta (smešta se u fajl predmeti.json), i api za preuzimanje svih prijavljenih studenata za predmet, prosleđuje se deo putanje kojoj će se programski dodavati šifra predmeta. Skripta preuzima podatke o prijavljenim studentima samo za predmete koji se slušaju u semestru (predmeti popunjeni u koraku 4). Predmeti se uparuju po nazivu, može se desiti da se naziv predmeta iz mejl liste i naziv predmeta iz rasporeda ne poklapaju, u tom slučaju se neće dobro povezati studenti za predmet. Skripta ispisuje nepostojeće predmete, to su predmeti koji se nalaze u rasporedu za semestar, a za koje ne postoji mejl lista, znači da se vereovatno nazivi ne poklapaju. Ukoliko ima nepostojećih predmeta, potrebno je ručno u fajlu predmeti.json promeniti ime predmeta da se poklapa sa imenom iz rasporeda, obrisati iz baze direktno sve prethodno importovane studente za semestar (po id semestru u tabeli `student_predmet_semestar`) i ponovo pokrenuti skriptu `maillist_import.py`.    







