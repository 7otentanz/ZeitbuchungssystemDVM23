from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os
import json
from . import berichtarchitektur

speicherpfadJSON = "/var/www/static"

### FUNKTIONEN ZUR PARAMETERVERGABE ###

def loginPruefen(request):
	try:
		matrikelnummer = request.session["matrikelnummer"]
		semester = request.session["semester"]
		berechtigung = request.session["berechtigung"]
	except:
		matrikelnummer = "Nicht angemeldet!"
		semester= "Nicht angemeldet!"
		berechtigung = "Nicht angemeldet!"
	parameter = {"berechtigung": berechtigung, "matrikelnummer": matrikelnummer, "semester": semester}
	return parameter

def nutzerberichte(request):
	matrikelnummer = request.session["matrikelnummer"]
	jsonDatei = os.path.join(speicherpfadJSON, "Nutzerberichte", f"berichte_{matrikelnummer}.json")
	alleBerichte = []
	try:
		with open(jsonDatei, "r", encoding="utf-8") as datei:
			daten = json.load(datei)
			alleBerichte = daten.get("Berichte", [])
	except:
		alleBerichte = []
	parameter = {"alleBerichte": alleBerichte}
	return parameter

def berechtigungsantraege(request):
	jsonDatei = os.path.join(speicherpfadJSON, "berechtigungsantraege.json")
	with open(jsonDatei, "r", encoding="utf-8") as datei:
		daten = json.load(datei)
		antraege = daten["Anträge"]
	jsonDatei = os.path.join(speicherpfadJSON, "nutzerdatenbank.json")
	with open(jsonDatei, "r", encoding="utf-8") as datei:
		daten = json.load(datei)
		benutzer = daten["Benutzer"]
	parameter = {"Anträge": antraege, "Benutzer": benutzer}
	return parameter

### FUNKTIONEN DIE TEMPLATES LADEN UND MIT PARAMETERN VERSEHEN ###
def index(request):
	return woranarbeitestdu(request)

def woranarbeitestdu(request):
	parameter = loginPruefen(request)
	return render(request, 'woranArbeitestDu.html', parameter)

def erzaehlmirmehr(request):
	parameter = loginPruefen(request)
	parameter.update(nutzerberichte(request))
	return render(request, 'erzaehlMirMehr.html', parameter)

def kuerzlichabgeschlossen(request):
	parameter = loginPruefen(request)
	parameter.update(nutzerberichte(request))
	return render(request, 'kuerzlichAbgeschlossen.html', parameter)

def lassmichdaszusammenfassen(request):
	parameter = loginPruefen(request)
	parameter.update(nutzerberichte(request))
	return render(request, 'lassMichDasZusammenfassen.html', parameter)

def nutzerverwaltung(request):
	parameter = loginPruefen(request)
	parameter.update(berechtigungsantraege(request))
	return render(request, 'nutzerverwaltung.html', parameter)

def login(request):
	return render(request, 'login.html')

def registrieren(request):
	return render(request, 'registrieren.html')

### FUNKTIONEN DIE FUNKTIONALITÄTEN ABBILDEN ###

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

### Nutzer abmelden ###

def nutzerAbmelden(request):

	request.session.flush()
	parameter = loginPruefen(request)

	return render(request, "woranArbeitestDu.html", parameter)

### Datetime Objekt absetzen ###

def berichtAnlegen(request):

	if request.method == "POST":
		
		startzeit = datetime.now()
		teilmodul = request.POST.get("teilmodul")
		matrikelnummer = request.session["matrikelnummer"]

		jsonDatei = os.path.join(speicherpfadJSON, "Nutzerberichte", f"berichte_{matrikelnummer}.json")

		try:
			with open(jsonDatei, "r", encoding="utf-8") as datei:
				daten = json.load(datei)
				bestehendeBerichte = daten.get("Berichte", [])

		except:
			bestehendeBerichte = []

		neuerBericht = berichtarchitektur.Bericht(startzeit, teilmodul)
		aktualisierteBerichte = neuerBericht.serialisierenalsjson(bestehendeBerichte)
		
		with open(jsonDatei, "w", encoding="utf-8") as datei:
			json.dump({"Berichte": aktualisierteBerichte}, datei, indent=4)

	return redirect("woranArbeitestDu")

### Berechtigungsantrag verschicken, für alle, die noch nicht Admin sind ###

def berechtigungsantrag(request):

	if request.method =="POST":

		jsonDatei = os.path.join(speicherpfadJSON, "berechtigungsantraege.json")

		berechtigung = request.session["berechtigung"]
		matrikelnummer = request.session["matrikelnummer"]

		if berechtigung == "nutzer":
			antragAls = "vip"
		elif berechtigung == "vip":
			antragAls = "admin"
		elif berechtigung == "gesperrt":
			antragAls = "nutzer"

		with open(jsonDatei, "r", encoding="utf-8") as datei:
			
			daten = json.load(datei)

			if matrikelnummer in daten["Anträge"]:
				daten["Anträge"][matrikelnummer] = antragAls

			else:
				daten["Anträge"][matrikelnummer] = antragAls


		with open(jsonDatei, "w", encoding="utf-8") as datei:
			json.dump(daten, datei, indent=4)

		return redirect("nutzerverwaltung")

def antragEntfernen(request):

	jsonDatei = os.path.join(speicherpfadJSON, "berechtigungsantraege.json")

	with open(jsonDatei, "r", encoding="utf-8") as datei:
			
		daten = json.load(datei)
		print(daten)
		matrnummer = request.POST.get("matrikelnummer")
		daten["Anträge"].pop(matrnummer)
		
	with open(jsonDatei, "w", encoding="utf-8") as datei:
		json.dump(daten, datei, indent=4)

def antragAblehnen(request):
	
	if request.method =="POST":

		antragEntfernen(request)

		return redirect("nutzerverwaltung")

def antragGenehmigen(request):

	if request.method =="POST":

		matrnummer = request.POST.get("matrikelnummer")

		jsonDatei = os.path.join(speicherpfadJSON, "nutzerdatenbank.json")

		with open(jsonDatei, "r", encoding="utf-8") as datei:
			daten = json.load(datei)

			if daten["Benutzer"][matrnummer]["berechtigung"] == "nutzer":
				daten["Benutzer"][matrnummer]["berechtigung"] = "vip"
			
			elif daten["Benutzer"][matrnummer]["berechtigung"] == "vip":
				daten["Benutzer"][matrnummer]["berechtigung"] = "admin"

			elif daten["Benutzer"][matrnummer]["berechtigung"] == "gesperrt":
				daten["Benutzer"][matrnummer]["berechtigung"] = "nutzer"
		
		with open(jsonDatei, "w", encoding="utf-8") as datei:
			json.dump(daten, datei, indent=4)
		
		antragEntfernen(request)

		return redirect("nutzerverwaltung")
			
def nutzersperren(request):

	if request.method =="POST":

		matrnummer = request.POST.get("matrikelnummer")

		jsonDatei = os.path.join(speicherpfadJSON, "nutzerdatenbank.json")

		with open(jsonDatei, "r", encoding="utf-8") as datei:
			daten = json.load(datei)

			daten["Benutzer"][matrnummer]["berechtigung"] = "gesperrt"
		
		with open(jsonDatei, "w", encoding="utf-8") as datei:
			json.dump(daten, datei, indent=4)

		return redirect("nutzerverwaltung")