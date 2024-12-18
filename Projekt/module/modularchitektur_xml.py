#import xml
from lxml import etree

class Modulgruppe:
    def __init__(self, name, index, module=[]):
        self.name = name
        self.module = module
        self.zeit = list()
        self.bericht = list()
        self.index = index
        self.modulgruppennummer = self.index.split(".")
    
    def modulHinzufuegen(self, modul):
        if modul.modulnummer[0] == self.modulgruppennummer[0]:
            self.module.append(modul)
        

    def aufgewendeteZeitenhinzufuegen(self, Zeiteintragobjekt):      #Zeit muss irgendwo her kommen. Soll aber schon direkt für das Teilmodul getrackt werden und dann den übergeorndeten auch hinzugefügt werden.
        self.zeit.append(Zeiteintragobjekt.zeit)


class Modul:
    def __init__(self, name, modulgruppe, index, teilmodule=[]):
        self.name = name
        self.modulgruppe = modulgruppe
        self.teilmodule = teilmodule
        self.zeit = list()
        self.index = index
        self.modulnummer = self.index.split(".")  # Hier die Nummer X2 von X1.X2.X3 definieren

    def teilmodulHinzufuegen(self, teilmodul):
        if teilmodul.modulnummer[1] == self.modulnummer[1]:
            self.teilmodule.append(teilmodul)
    def aufgewendeteZeitenhinzufuegen(self, Zeiteintragobjekt):      #Zeit muss irgendwo her kommen. Soll aber schon direkt für das Teilmodul getrackt werden und dann den übergeorndeten auch hinzugefügt werden.
        self.zeit.append(Zeiteintragobjekt.zeit)
        self.modulgruppe.aufgewendeteZeitenhinzufuegen(Zeiteintragobjekt)   #auf die Methode der Modulgruppe des Moduls zugreifen
        # Auf die richtige MODULGRUPPE zugreifen und der die Zeiten auch noch hinzufügen.


class Teilmodul:
    def __init__(self, name, modul, index):
        self.name = name
        self.modul = modul
        self.zeit = list()
        self.index = index
        self.teilmodulnummer = self.index.split(".")

    def aufgewendeteZeitenhinzufuegen(self, Zeiteintragobjekt):      #Zeit muss irgendwo her kommen. Soll aber schon direkt für das Teilmodul getrackt werden und dann den übergeorndeten auch hinzugefügt werden.
        self.zeit.append(Zeiteintragobjekt.zeit)

        if self.modul.modulnummer [0] == self.teilmodulnummer [0] and self.modul.modulnummer [1] == self.teilmodulnummer [1]:
            self.modul.aufgewendeteZeitenhinzufuegen(Zeiteintragobjekt)     #auf die Methode des Moduls des Teilmoduls zugreifen
        if self.modul.modulgruppe.modulgruppennummer [0] == self.modul.modulnummer [0]:
            self.modul.modulgruppe.aufgewendeteZeitenhinzufuegen(Zeiteintragobjekt)
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

moduluebersicht = open("Moduleuebersicht.xml", encoding="utf-8").read()
moduluebersicht_xml = etree.fromstring(moduluebersicht)


for modulgruppen_element in moduluebersicht_xml.iter("Modulgruppe"):
    modulgruppen_name = modulgruppen_element.attrib["name"]
    modulgruppen_nummer = modulgruppen_element.attrib["index"]
    if modulgruppen_name not in modulgruppen:
        modulgruppen[modulgruppen_name] = Modulgruppe(modulgruppen_name, modulgruppen_nummer)
    modulgruppen_objekt = modulgruppen[modulgruppen_name]
    #print(modulgruppen_objekt.name)
    


for modul_element in moduluebersicht_xml.iter("Modul"):
    modul_name = modul_element.attrib["name"]
    modul_nummer = modul_element.attrib["index"]
    if modul_name not in module:
        module[modul_name] = Modul(modul_name, modulgruppen_objekt, modul_nummer)
    modul_objekt = module[modul_name]
    modulgruppen_objekt.modulHinzufuegen(modul_objekt)
    
    #print(modul_objekt.name)


for teilmodul_element in moduluebersicht_xml.iter("Teilmodul"):
    teilmodul_name = teilmodul_element.attrib["name"]
    teilmodul_nummer = teilmodul_element.attrib["index"]
    if teilmodul_name not in teilmodule:
        teilmodule[teilmodul_name] = Teilmodul(teilmodul_name, modul_objekt, teilmodul_nummer)



print(modulgruppen)

fach = ("Vertiefung Informatik")

print("\nInhalt des Dictionaries 'modulgruppen':")
for semf, value in modulgruppen.items():
    print(f"- Keyname: {semf}, Valuename: {value.name}, Anzahl der Module: {len(value.module)}")


print("\nInhalt des Dictionaries 'Module':")
for key, value in module.items():
    print(f"- Keyname: {key}, Valuename: {value.name}, Anzahl der Teilmodule: {len(value.teilmodule)}")



print("\nInhalt des Dictionaries 'Teilmodule':")
for key, value in teilmodule.items():
    print(f"- Keyname: {key}, Valuename: {value.name}")

    