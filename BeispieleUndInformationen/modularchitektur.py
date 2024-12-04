import csv

class Modulgruppe:
    def __init__(self, name, module=[]):
        self.name = name
        self.module = module
        self.zeit = list()
        self.bericht = list()
        self.modulnummer = self.name.split(".")
    
    def modulHinzufuegen(self, modul):
        if modul.modulnummer[0] == self.modulnummer[0]:
            #print(f"{modul.modulnummer[0]} ist angeblich gleich {self.modulnummer[0]}")
            #print(f"{modul.name} wurde {self.name} hinzugefügt!")
            self.module.append(modul)
        elif modul.modulnummer[0] != self.modulnummer[0]:
            print("kann niemals passieren, weil beim erstellen jede zeile durchiteriert wird - und die stimmen immer überein.")
        else:
            print("kann niemals passieren, weil beim erstellen jede zeile durchiteriert wird - und die stimmen immer überein.")

    def aufgewendeteZeitenhinzufuegen(self, Zeiteintragobjekt):      #Zeit muss irgendwo her kommen. Soll aber schon direkt für das Teilmodul getrackt werden und dann den übergeorndeten auch hinzugefügt werden.
        self.zeit.append(Zeiteintragobjekt.zeit)


class Modul:
    def __init__(self, name, modulgruppe, teilmodule=[]):
        self.name = name
        self.modulgruppe = modulgruppe
        self.teilmodule = teilmodule
        self.zeit = list()
        self.modulnummer = self.name.split(".")  # Hier die Nummer X2 von X1.X2.X3 definieren

    def teilmodulHinzufuegen(self, teilmodul):
        if teilmodul.modulnummer[1] == self.modulnummer[1]:
            #print(f"{teilmodul.modulnummer[1]} ist tatsächlich gleich {self.modulnummer[1]}")
            #print(f"{teilmodul.name} wurde {self.name} hinzugefügt!")
            self.teilmodule.append(teilmodul)
        elif teilmodul.modulnummer[1] != self.modulnummer[1]:
            print("kann niemals passieren, weil beim erstellen jede zeile durchiteriert wird - und die stimmen immer überein.")
        else:
            print("kann niemals passieren, weil beim erstellen jede zeile durchiteriert wird - und die stimmen immer überein.")
        
    def aufgewendeteZeitenhinzufuegen(self, Zeiteintragobjekt):      #Zeit muss irgendwo her kommen. Soll aber schon direkt für das Teilmodul getrackt werden und dann den übergeorndeten auch hinzugefügt werden.
        self.zeit.append(Zeiteintragobjekt.zeit)
        self.modulgruppe.aufgewendeteZeitenhinzufuegen(Zeiteintragobjekt)   #auf die Methode der Modulgruppe des Moduls zugreifen
        # Auf die richtige MODULGRUPPE zugreifen und der die Zeiten auch noch hinzufügen.


class Teilmodul:
    def __init__(self, name, modul):
        self.name = name
        self.modul = modul
        self.zeit = list()
        self.modulnummer = self.name.split(".")

    def aufgewendeteZeitenhinzufuegen(self, Zeiteintragobjekt):      #Zeit muss irgendwo her kommen. Soll aber schon direkt für das Teilmodul getrackt werden und dann den übergeorndeten auch hinzugefügt werden.
        self.zeit.append(Zeiteintragobjekt.zeit)
        self.modul.aufgewendeteZeitenhinzufuegen(Zeiteintragobjekt)     #auf die Methode des Moduls des Teilmoduls zugreifen
        # auf das richtige MODUL zugreifen und dem die Zeiten auch noch hinzufügen


class Zeiteintrag:
    def __init__(self, zeit, modul, bericht):
        self.zeit = zeit
        self.modul = modul
        self.bericht = bericht

    def zeitAusrechnen(self, startzeit, endzeit):       # startzeit und endzeit muss übergeben werden, aus der html heraus
        zeit = endzeit - startzeit                      # sicherstellen, dass es minuten sind
        return zeit
    
    def zeiteintragEinemModulHinzufuegen(self, modul):
        modul.aufgewendeteZeitenHinzufuegen(self)


class Semester:

    # das Semester soll die Übersicht die klickbaren Module beinhalten. Das Semester soll aus allen "kleinsten Einheiten" bestehen, denen dann Zeiten zugewiesen werden.
    # das Semester soll in der Übersicht von Nutzer neu angelegt werden können
    # soll später ermöglichen den Zeitaufwand für das ganze Semester anzuzeigen, welches im Voraus festgelegt wurde

    def __init__(self):
        self.teilmodule = list()

    def teilmodulHinzufuegen(self, teilmodul):
        self.teilmodule.append(teilmodul)

modulgruppen = dict()
module = dict()
teilmodule = dict()

with open("./BeispieleundInformationen/moduluebersicht.csv", "r", encoding="utf-8-sig") as moduluebersicht:
    modulreader = csv.DictReader(moduluebersicht, delimiter=";")
    for zeile in modulreader:
            teilmodulname = zeile["Teilmodul"]
            modulname = zeile["Modul"]
            modulgruppenname = zeile["Modulgruppe"]
            
            if modulgruppenname not in modulgruppen:
                modulgruppen[modulgruppenname] = Modulgruppe(modulgruppenname)
            else:
                pass
            modulgruppe = modulgruppen[modulgruppenname]
            
            if modulname not in module:
                module[modulname] = Modul(modulname, modulgruppe)
                modulgruppe.modulHinzufuegen(module[modulname])
            else:
                pass
            modul = module[modulname]

            if teilmodulname not in teilmodule:
                teilmodule[teilmodulname] = Teilmodul(teilmodulname, modul)
                modul.teilmodulHinzufuegen(teilmodule[teilmodulname])
            else:
                pass
            teilmodul = teilmodule[teilmodulname]

modulgruppe2 = modulgruppen["1. Technische Dimension der Digitalisierung"]

#print(modulgruppe2.name)       # Hier wird die richtige Modulgruppe (bzw. ihr Name) geprintet. Passt.

module2 = modulgruppe2.module

for inhalt in module2:         # Hier soll die Liste aller Module dieser Modulgruppe geprintet werden. ANGEBLICH SIND DA ABER ALLE DRIN! Passt nicht.
    print(inhalt.name)

modul2 = module2[4]

#print(modul2.name)

teilmodule2 = modul2.teilmodule

#for inhalt in teilmodule2:
    #print(inhalt.name)

teilmodul2 = teilmodule2[0]

#print(teilmodul2.name)




# BUTTON
# 1. Klick - Teilmodul raussuchen, startzeit definiert
# 2. Klick - Endzeit definiert werden, mit Startzeit und Endzeit Zeiteintrag.zeitAusrechen(var1, var2)