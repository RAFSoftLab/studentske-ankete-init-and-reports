
### Softver za pripremu podataka za anketiranje studenata o predmetima i nastavnicima, obradu podataka i generisanje raznih vrsta izveštaja

Projekat sadrži skripte za pripremu podataka za anketrianje za veb aplikaciju dostupnu na: https://github.com/RAFSoftLab/studentske-ankete-webapp


#### Priprema baze za anketiranje

Prvo podizanje baze

1. Kreirati bazu na serveru (MySQL)

2. Upisati sve podatke potrebne za konekciju u `databaseconfig.py` u promenljivu `mysqlParams`

3. Pokrenuti skriptu  `database_init.py`, skripta pravi tabele i importuje pitanja za anketu

Priprema podataka za anketiranje za jedan semestar

4. Import podataka iz rasporeda (koji nastavnik drži koji predmet u semestru), zadaje se školska godina, semestar (z-zimski, l-letnji) i putanja do fajla sa rasporedom za semestar (csv fajl), primer poziva:

   `python import_semester_data.py "2020/2021" z csv`

5. Posle izvršene skripte u prethodnom koraku na stdout se ispisuje dodeljeni id semestra za koji se priprema anketiranje, taj broj upisati ručno u `databaseconfig.py` u promenljivu `trenutni_semestar` 

6. Importovati podatke o studentima koji slušaju predmete, ovi podaci se u sadašnjoj verziji importuju iz mejl listi pomoću skripte `maillist_import.py`. Prosleđuju se dve url putanje, api za preuzimanje svih predmeta (smešta se u fajl predmeti.json), i api za preuzimanje svih prijavljenih studenata za predmet, prosleđuje se deo putanje kojoj će se programski dodavati šifra predmeta. Skripta preuzima podatke o prijavljenim studentima samo za predmete koji se slušaju u semestru (predmeti popunjeni u koraku 4). Predmeti se uparuju po nazivu, može se desiti da se naziv predmeta iz mejl liste i naziv predmeta iz rasporeda ne poklapaju, u tom slučaju se neće dobro povezati studenti za predmet. Skripta ispisuje nepostojeće predmete, to su predmeti koji se nalaze u rasporedu za semestar, a za koje ne postoji mejl lista, znači da se verovatno nazivi ne poklapaju. Ukoliko ima nepostojećih predmeta, potrebno je ručno u fajlu predmeti.json promeniti ime predmeta da se poklapa sa imenom iz rasporeda, obrisati iz baze direktno sve prethodno importovane studente za semestar (po id semestru u tabeli `student_predmet_semestar`) i ponovo pokrenuti skriptu `maillist_import.py`.    

#### Izveštaji

Nakon završenog anketiranja, generišu se izveštaji za sajt i pdf-ovi koji se šalju nastavnicima na mejl. Izveštaji za sajt se generišu kao povezane php stranice koje u zaglavlju imaju proveru za logovanje preko raf.rs naloga. Postoji nekoliko podržanih formata izveštaja. 

- `report-public-subjects.py` - generiše izveštaj koji sadrži rezultate samo za predmete i opšta pitanja za Fakultet
- `report-public-minimal.py` - generiše izveštaj sa tabelom o prosečnim ocenama i brojem anketiranih studenata za sve predmete iz semestra
- `report-public.py` - generiše kompletan izveštaj sa svim komentarima i ocenama za predmete i nastavnike

Generisanje izveštaja za nastavnike u pdf-u i slanje na mejl se radi preko skripte `report.py`, potreban je token.json za gmail autentifikaciju. Svaki profesor dobija izveštaj za svoje predmete, za sebe i za sve asistente i saradnike na predmetu, uključujući ocene i komentare, asistenti i saradnici dobijaju svoje ocene i komentare. 


Napomena: pre poziva skripti za generisanje izveštaja u fajlu `report_queries.py` podesiti vrednosti promenljivih 
- `pitanja_min` - postaviti id prvog pitanja iz baze koji se koristi za anketiranje, ovo može biti 0 ili ako se menjaju pitanja, obično se dodaju na postojeća, onda se stavlja id prvog novog dodatog pitanja, ne treba brisati prethodna pitanja, jer su ranije ankete za njih vezane
- `pitanje_id_nastavnik` - id bilo kog pitanja koje se odnosi na nastavnika
- `pitanje_id_predmet` - id bilo kog pitanja koje se odnosi na predmet







