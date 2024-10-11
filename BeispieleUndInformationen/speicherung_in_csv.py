import csv
import os

class Arbeitsbereich:
    def __init__(self,  datum_A, startzeit_A, endzeit_A, module_A, text_A):
        self.datum = datum_A
        self.startzeit = startzeit_A
        self.endzeit = endzeit_A

        self.module = module_A
        self.text = text_A
    
    def __str__(self): #braucht man, um print befehl außerhalb der klasse zu nutzen
        return f"Datum: {self.datum} \nStartzeit: {self.startzeit}, Endzeit: {self.endzeit} \nModul: {self.module}, Text: {self.text}"

    def arbeitszeiten(self):
        pass

    def modulzuehörigkeit(self):
        pass

    def tätigkeiten(self):
        pass

class Personen:
    def __init__(self, vorname_P, nachname_P, matnr_P, jg_P, berechtigung_P):
        self.__name = f"{nachname_P}, {vorname_P}"
        self.__vorname = vorname_P
        self.__nachname = nachname_P
        self.__matnr = matnr_P
        self.__jg = jg_P
        self.__berechtigung = berechtigung_P

    def __str__(self): #braucht man, um print befehl außerhalb der klasse zu nutzen

        #return f"Name: {self.__name} \nMat.Nr.: {self.__matnr}, Jahrgang: {self.__jg} \nGruppe: {self.__gruppe}"
        return f"Name: {self.__nachname}, {self.__vorname} \nMat.Nr.: {self.__matnr}, Jahrgang: {self.__jg} \nGruppe: {self.__berechtigung}"
    
    def in_csv_schreiben_person(self, dateiname):
        with open (dateiname, "a", newline='', encoding = "utf-8") as file:
            writer = csv.writer(file, delimiter= ";" )
            writer.writerow([self.__vorname, self.__nachname, self.__matnr, self.__jg, self.__berechtigung])


class Gruppenzugehörigkeit:
    def __init__(self, andwender_G, vip_G, admin_G):
        self.__anwender = andwender_G
        self.__vip = vip_G
        self.__admin = admin_G




def get_lowercase(eingabe):
    eingabe = eingabe.lower()
    return eingabe

def abfragen_person():
    vorname = input("Gib den Vornamen ein: ")
    nachname = input ("Gib den Nachnamen ein: ")
    mat_nr = input ("Gib die Mat. Nr. ein: ")
    jahrgang = input ("Gib den Jahrgang ein ein: ")
    berechtigung = input ("Wähle eine Berechtigung: Benutzer [b], VIP [v] oder Administrator [a] ")
    berechtigung = get_lowercase(berechtigung)

    while berechtigung != "b" and berechtigung != "v" and berechtigung != "a":
        print("Die Eingabe war leider falsch, bitte erneut probieren.")
        berechtigung = input ("Wähle eine Berechtigung: Benutzer [b], VIP [v] oder Administrator [a] ")
        berechtigung = get_lowercase(berechtigung)

    if berechtigung == "b":
        berechtigung = "Benutzer"
    elif berechtigung == "v":
        berechtigung ="VIP"
    elif berechtigung == "a":
        berechtigung == "Administrator"

    return Personen(vorname, nachname, mat_nr, jahrgang, berechtigung)

def schreibe_header():
    if not os.path.exists(dateiname):
        with open(dateiname, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["Vorname", "Nachname", "Mat. Nr.", "Jahrgang", "Berechtigung"])


dateiname = "Personenverzeichnis.csv"
schreibe_header()

q_person_anlegen = input("Neue Person anlegen? [y/n]")
q_person_anlegen = get_lowercase(q_person_anlegen)

if q_person_anlegen == "y":
    
    person1 = abfragen_person()

person1.in_csv_schreiben_person(dateiname)

