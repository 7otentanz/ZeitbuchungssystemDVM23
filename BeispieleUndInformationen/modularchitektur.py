import csv

class Modulgruppe:
    def __init__(self, name, module=[]):
        self.name = name
        self.module = module
        self.zeit = list()
        self.bericht = list()
        self.modulnummer = self.name.split(".")[0]
    
    def modulHinzufuegen(self, modul):
        self.module.append(modul)

    def aufgewendeteZeitenhinzufuegen(self, Zeiteintragobjekt):      #Zeit muss irgendwo her kommen. Soll aber schon direkt für das Teilmodul getrackt werden und dann den übergeorndeten auch hinzugefügt werden.
        self.zeit.append(Zeiteintragobjekt.zeit)


class Modul:
    def __init__(self, name, modulgruppe, teilmodule=[]):
        self.name = name
        self.modulgruppe = modulgruppe
        self.teilmodule = teilmodule
        self.zeit = list()
        self.modulnummer = self.name.split(".")[1]  # Hier die Nummer X2 von X1.X2.X3 definieren

    def teilmodulHinzufuegen(self, teilmodul):
        self.teilmodule.append(teilmodul)
        
    def aufgewendeteZeitenhinzufuegen(self, Zeiteintragobjekt):      #Zeit muss irgendwo her kommen. Soll aber schon direkt für das Teilmodul getrackt werden und dann den übergeorndeten auch hinzugefügt werden.
        self.zeit.append(Zeiteintragobjekt.zeit)
        self.modulgruppe.aufgewendeteZeitenhinzufuegen(Zeiteintragobjekt)   #auf die Methode der Modulgruppe des Moduls zugreifen
        # Auf die richtige MODULGRUPPE zugreifen und der die Zeiten auch noch hinzufügen.


class Teilmodul:
    def __init__(self, name, modul):
        self.name = name
        self.modul = modul
        self.zeit = list()

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
            
            if modulgruppenname in modulgruppen:
                pass
            else:
                modulgruppen[modulgruppenname] = Modulgruppe(modulgruppenname)
            modulgruppe = modulgruppen[modulgruppenname]
            
            if modulname in module:
                pass
            else:
                module[modulname] = Modul(modulname, modulgruppe)
                modulgruppe.modulHinzufuegen(module[modulname])
            modul = module[modulname]

            if teilmodulname in teilmodule:
                pass
            else:
                teilmodule[teilmodulname] = Teilmodul(teilmodulname, modul)
                modul.teilmodulHinzufuegen(teilmodule[teilmodulname])
            teilmodul = teilmodule[teilmodulname]

# Ergebnisse ausgeben
print("Modulgruppen:")
for modulgruppe in modulgruppen.values():
    print(f"- {modulgruppe.name} ({len(modulgruppe.module)} Module)")

print("\nModule:")
for modul in module.values():
    print(f"- {modul.name} ({len(modul.teilmodule)} Teilmodule, gehört zu {modul.modulgruppe.name})")

print("\nTeilmodule:")
for teilmodul in teilmodule.values():
    print(f"- {teilmodul.name} (gehört zu {teilmodul.modul.name})")

# Infos aus den CSV Spalten?

# Alle Modulgruppen erstellen
# Alle Module erstellen + Modulgruppen definieren.
# Alle Teilmodule erstellen + Module definieren





# BUTTON
# 1. Klick - Teilmodul raussuchen, startzeit definiert
# 2. Klick - Endzeit definiert werden, mit Startzeit und Endzeit Zeiteintrag.zeitAusrechen(var1, var2)