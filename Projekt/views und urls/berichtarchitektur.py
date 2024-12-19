import uuid
from datetime import datetime

class Bericht:

    def __init__(self, startzeit, teilmodul, endzeit = 0, text = "", arbeitszeit = 0):
        self.startzeit = startzeit
        self.teilmodul = teilmodul
        self.endzeit = endzeit
        self.text = text
        self.arbeitszeit = arbeitszeit
        self.id = uuid.uuid4()

    def zeitBeenden(self, endzeit):
        self.endzeit = endzeit
        self.arbeitszeit = self.endzeit - self.startzeit
    
    def textEinfuegen(self, text):
        self.text = text