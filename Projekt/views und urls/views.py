from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
import smtplib
from email.message import EmailMessage
import socket
import os
import json

speicherpfadJSON = "/var/www/static"

def woranarbeitestdu(request):

	try:
		matrikelnummer = request.session["matrikelnummer"]
		semester = request.session["semester"]
		berechtigung = request.session["berechtigung"]
	except:
		matrikelnummer = "Nicht angemeldet!"
		semester= "Nicht angemeldet!"
		berechtigung = "Nicht angemeldet!"

	return render(request, 'woranArbeitestDu.html', {"berechtigung": berechtigung, "matrikelnummer": matrikelnummer, "semester": semester})

def erzaehlmirmehr(request):

	try:
		matrikelnummer = request.session["matrikelnummer"]
		semester = request.session["semester"]
		berechtigung = request.session["berechtigung"]
	except:
		matrikelnummer = "Nicht angemeldet!"
		semester= "Nicht angemeldet!"
		berechtigung = "Nicht angemeldet!"

	return render(request, 'erzaehlMirMehr.html', {"berechtigung": berechtigung, "matrikelnummer": matrikelnummer, "semester": semester})

def kuerzlichabgeschlossen(request):

	try:
		matrikelnummer = request.session["matrikelnummer"]
		semester = request.session["semester"]
		berechtigung = request.session["berechtigung"]
	except:
		matrikelnummer = "Nicht angemeldet!"
		semester= "Nicht angemeldet!"
		berechtigung = "Nicht angemeldet!"

	return render(request, 'kuerzlichAbgeschlossen.html', {"berechtigung": berechtigung, "matrikelnummer": matrikelnummer, "semester": semester})

def lassmichdaszusammenfassen(request):

	try:
		matrikelnummer = request.session["matrikelnummer"]
		semester = request.session["semester"]
		berechtigung = request.session["berechtigung"]
	except:
		matrikelnummer = "Nicht angemeldet!"
		semester= "Nicht angemeldet!"
		berechtigung = "Nicht angemeldet!"

	return render(request, 'lassMichDasZusammenfassen.html', {"berechtigung": berechtigung, "matrikelnummer": matrikelnummer, "semester": semester})

def nutzerverwaltung(request):

	try:
		matrikelnummer = request.session["matrikelnummer"]
		semester = request.session["semester"]
		berechtigung = request.session["berechtigung"]
	except:
		matrikelnummer = "Nicht angemeldet!"
		semester= "Nicht angemeldet!"
		berechtigung = "Nicht angemeldet!"

	return render(request, 'nutzerverwaltung.html', {"berechtigung": berechtigung, "matrikelnummer": matrikelnummer, "semester": semester})

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
				berechtigung = daten["Benutzer"][matrikelnummer]["berechtigung"]
				request.session["berechtigung"] = berechtigung
				
				return render(request, "woranArbeitestDu.html", {"berechtigung": berechtigung, "matrikelnummer": matrikelnummer, "semester": semester})
			
			elif passwort != daten["Benutzer"][matrikelnummer]["passwort"]:
				return HttpResponse("<script>alert('Falsches Passwort!');window.history.back()</script>")
			
		if matrikelnummer not in daten["Benutzer"]:
			return HttpResponse("<script>alert('Du musst dich zuerst registrieren!');window.history.back()</script>")

### Datetime Objekt absetzen ###

def zeitGeben(request):

	if request.method == "POST":
		jetzt = datetime.now()
		print(jetzt)

	try:
		matrikelnummer = request.session["matrikelnummer"]
		semester = request.session["semester"]
		berechtigung = request.session["berechtigung"]
	except:
		matrikelnummer = "Nicht angemeldet!"
		semester= "Nicht angemeldet!"
		berechtigung = "Nicht angemeldet!"

	return render(request, 'woranArbeitestDu.html', {"berechtigung": berechtigung, "matrikelnummer": matrikelnummer, "semester": semester})

### Berechtigungsantrag verschicken, für alle, die noch nicht Admin sind ###

def berechtigungsantrag(request):

	if request.method =="POST":

		berechtigung = request.session["berechtigung"]
		matrikelnummer = request.session["matrikelnummer"]
		semester = request.session["semester"]

		if berechtigung == "nutzer":
			antragAls = "vip"
		elif berechtigung == "vip":
			antragAls = "admin"
		
		# JSON erstellen mit allen Berichten!? oder die auch in die Nutzer mit rein!? 

		#### Scheinbar blockiert der Server selbst die Verbindung zum SMTP Server... ####

		# s = smtplib.SMTP(host="213.165.67.124", port=587)
		# s.starttls()
		# s.login("tenpm@web.de", "Mindestens9Zeichen!")

		# msg = EmailMessage()
		# msg["From"] = "tenpm@web.de"
		# msg["To"] = "t_hauser@web.de"
		# msg["Subject"] = f"Antrag von {matrikelnummer}"
		# msg.set_content(f"Guten Tag liebe Admins,\nder Nutzer {matrikelnummer} hat einen Antrag auf {antragAls} gestellt.\nDer Antrag liegt in ihrer Nutzerverwaltung zur Zustimmung bereit!")

		# s.send_message(msg)

		# s.quit()

		return render(request, 'nutzerverwaltung.html', {"berechtigung": berechtigung, "matrikelnummer": matrikelnummer, "semester": semester})
