# Dieses Script speichert die Inhalte der "Modulübersicht.csv" in eine SQL-Datenbank. Ob wir das brauchen? Keine Ahnung, vielleicht?

import sqlite3
import csv
import os

dateipfadCSV = "./BeispieleUndInformationen/moduluebersicht.csv"            # Hier den korrekten Pfad angeben
dateipfadSQL = "./BeispieleUndInformationen/moduluebersicht.db"             # Hier den korrekten Pfad angeben

connect = sqlite3.connect(dateipfadSQL)
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS moduluebersicht (
                Modulgruppe TEXT,
                Modul TEXT,
                Teilmodul TEXT)""")

with open(os.path.join(os.getcwd(), dateipfadCSV), "r") as moduluebersichtCSV:
    text = csv.reader(moduluebersichtCSV, delimiter=";")
    next(text, None)                                                        # ignoriert den Header

    for zeile in text:
        while len(zeile) < 3:
            zeile.append("")
        
        cursor.execute("INSERT INTO moduluebersicht (Modulgruppe, Modul, Teilmodul) VALUES (?, ?, ?)", zeile)

connect.commit()
connect.close() 