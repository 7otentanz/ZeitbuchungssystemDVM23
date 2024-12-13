from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
import os
import json

speicherpfadJSON = "/var/www/static"

def woranarbeitestdu(request):
	return render(request, 'woranArbeitestDu.html')

def erzaehlmirmehr(request):
	return render(request, 'erzaehlMirMehr.html')

def kuerzlichabgeschlossen(request):
	return render(request, 'kuerzlichAbgeschlossen.html')

def lassmichdaszusammenfassen(request):
	return render(request, 'lassMichDasZusammenfassen.html')

def nutzerverwaltung(request):
	return render(request, 'nutzerverwaltung.html')

def login(request):
	return render(request, 'login.html')

def registrieren(request):
	return render(request, 'registrieren.html')

### Neuen Benutzer anlegen / registrieren ###

def nutzerRegistrieren(request):
	
	matrikelnummer = request.POST.get("matrikelnummer")
	vorname = request.POST.get("vorname")
	nachname = request.POST.get("nachname")
	jahrgang = request.POST.get("jahrgang")
	passwort = request.POST.get("passwort")
	berechtigung = "nutzer"
	
	startJahr = int(jahrgang[-2:]) + 2000
	heute = datetime.now()
	diesesJahr = heute.year
	dieserMonat = heute.month
	monateSeitBeginn = (diesesJahr - startJahr) * 12 + dieserMonat - 9
	
	semester = monateSeitBeginn // 6 + 1 

	nutzerDaten = {
		"matrikelnummer": matrikelnummer,
		"vorname": vorname,
		"nachname": nachname,
		"jahrgang": jahrgang,
		"semester": semester,
		"passwort": passwort,
		"berechtigung": berechtigung
	}

	jsonDatei = os.path.join(speicherpfadJSON, "nutzerdatenbank.json")

	with open(jsonDatei, "r", encoding="utf-8") as datei:
		daten = json.load(datei)

		if matrikelnummer in daten["Benutzer"]:
			return redirect("login")
		
		else:
			daten["Benutzer"][matrikelnummer] = nutzerDaten

	with open(jsonDatei, "w", encoding="utf-8") as datei:
		json.dump(daten, datei, indent=4)
	
	return redirect("login")

### Bestehenden Benutzer anmelden ###

def nutzerAnmelden(request):

	matrikelnummer = request.POST.get("matrikelnummer")
	passwort = request.POST.get("passwort")

	jsonDatei = os.path.join(speicherpfadJSON, "nutzerdatenbank.json")

	with open(jsonDatei, "r", encoding="utf-8") as datei:
		daten = json.load(datei)

		if matrikelnummer in daten["Benutzer"]:

			if passwort == daten["Benutzer"][matrikelnummer]["passwort"]:
				request.session["matrikelnummer"] = matrikelnummer		# erstellt eine session... die so lange aktiv bleibt, wie der browser geöffnet ist.
				semester = daten["Benutzer"][matrikelnummer]["semester"]
				request.session["semester"] = semester
				return redirect("woranArbeitestDu")
			
			elif passwort != daten["Benutzer"][matrikelnummer]["passwort"]:
				return HttpResponse("<script>alert('Falsches Passwort!');window.history.back()</script>")
			
		if matrikelnummer not in daten["Benutzer"]:
			return HttpResponse("<script>alert('Du musst dich zuerst registrieren!');window.history.back()</script>")

### Datetime Objekt annehmen ###

def zeitGeben(request):
	if request.method == "POST":
		jetzt = datetime.now()
		print(jetzt)

		### dann muss diese Zeit übermittelt werden an die modularchitektur.py... oder so!? ###

		return render(request, 'woranArbeitestDu.html')


	
