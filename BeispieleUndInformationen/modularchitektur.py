class Modulgruppe:
    def __init__(self, name):
        self.name = name
        self.module = list()
        self.zeit = list()
        self.modulnummer = self.name.split(".")[0]
    
    def modulHinzufuegen(self, modul):
        self.module.append(modul)

    def aufgewendeteZeitenhinzufuegen(self, zeit):      #Zeit muss irgendwo her kommen. Soll aber schon direkt für das Teilmodul getrackt werden und dann den übergeorndeten auch hinzugefügt werden.
        self.zeit.append(zeit)


class Modul:
    def __init__(self, name):
        self.name = name
        self.teilmodule = list()
        self.zeit = list()
        self.modulnummer = self.name.split(".")[1]  # Hier die Nummer X2 von X1.X2.X3 definieren
    
    def einerModulgruppeHinzufuegen(self, modulgruppe):
        modulname = self.name
        modulnummer = modulname.split(".")
        if modulnummer[0] == 1:                     # der Modulgruppe mit der Nummer X1 von X1.X2.X3 dieses Modul hinzufügen
            pass                                        # Hier muss das richtige MODULGRUPPE Objekt ausgewählt werden

    def teilmodulHinzufuegen(self, teilmodul):
        self.teilmodule.append(teilmodul)
        
    def aufgewendeteZeitenhinzufuegen(self, zeit):      #Zeit muss irgendwo her kommen. Soll aber schon direkt für das Teilmodul getrackt werden und dann den übergeorndeten auch hinzugefügt werden.
        self.zeit.append(zeit) 
        # Auf die richtige MODULGRUPPE zugreifen und der die Zeiten auch noch hinzufügen.


class Teilmodul:
    def __init__(self, name):
        self.name = name
        self.zeit = list()
    
    def einemModulHinzufuegen(self):
        teilmodulname = self.name
        teilmodulnummer = teilmodulname.split(".")
        if teilmodulnummer[1] == 1:                  # dem Modul mit der Nummer X2 von X1.X2.X3 dieses Teilmodul hinzufügen
            pass                                        # hier muss das richtige MODUL Objekt ausgewählt werden
    
    def aufgewendeteZeitenhinzufuegen(self, zeit):      #Zeit muss irgendwo her kommen. Soll aber schon direkt für das Teilmodul getrackt werden und dann den übergeorndeten auch hinzugefügt werden.
        self.zeit.append(zeit)
        # auf das richtige MODUL zugreifen und dem die Zeiten auch noch hinzufügen

class Semester:

    # das Semester soll die Übersicht die klickbaren Module beinhalten. Das Semester soll aus allen "kleinsten Einheiten" bestehen, denen dann Zeiten zugewiesen werden.
    # das Semester soll in der Übersicht von Nutzer neu angelegt werden können
    # soll später ermöglichen den Zeitaufwand für das ganze Semester anzuzeigen, welches im Voraus festgelegt wurde

    def __init__(self):
        self.teilmodule = list()

    def teilmodulHinzufuegen(self, teilmodul):
        self.teilmodule.append(teilmodul)
    

# Infos aus den CSV Spalten?

# Alle Teilmodule erstellen
# Alle Module erstellen
# Alle Modulgruppen erstellen
# Alle Teilmodule den richtigen Modulen hinzufügen
# Alle Module den richtigen Modulgruppen hinzufügen
