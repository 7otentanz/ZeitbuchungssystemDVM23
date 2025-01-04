import uuid
from datetime import datetime

class Bericht:

    alleBerichte = []

    def __init__(self, startzeit, teilmodul, endzeit = 0, text = "", arbeitszeit = 0):
        self.startzeit = startzeit
        self.teilmodul = teilmodul
        self.endzeit = endzeit
        self.text = text
        self.arbeitszeit = arbeitszeit
        self.id = uuid.uuid4()

    def zeitBeenden(self, endzeit):
        self.endzeit = endzeit
        
        if self.endzeit != 0:
            self.arbeitszeit = (self.endzeit - self.startzeit).total_secondes()/60
    
    def textEinfuegen(self, text):
        self.text = text
    
    def serialisierenalsjson(self, bestehendeBerichte=None):
        
        if self.endzeit == 0:
            endzeit = 0
        else:
            endzeit = self.endzeit.strftime("%R %d.%m.%y")

        berichtJSON = {
            "startzeit": self.startzeit.strftime("%R %d.%m.%y"),
            "teilmodul": self.teilmodul,
            "endzeit": endzeit,
            "text": self.text,
            "arbeitszeit": self.arbeitszeit,
            "id": str(self.id)
        }

        if bestehendeBerichte == None:
            bestehendeBerichte = []

        bestehendeBerichte.append(berichtJSON)
        Bericht.alleBerichte = bestehendeBerichte
        
        return Bericht.alleBerichte

    def serialisierenalscsv(self):
        pass

    def serialisierenalsxml(self):
        pass

