from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.middleware.csrf import get_token
import os
import json

def woranarbeitestdu(request):
	return render(request, 'woranArbeitestDu.html')

def erzaehlmirmehr(request):
	return render(request, 'erzaehlMirMehr.html')

def kuerzlichabgeschlossen(request):
	return render(request, 'kuerzlichAbgeschlossen.html')

def lassmichdaszusammenfassen(request):
	return render(request, 'lassMichDasZusammenfassen.html')

def login(request):
	return render(request, 'login.html')

def registrieren(request):
	return render(request, 'registrieren.html')

# Neuen Benutzer anlegen / registrieren

speicherpfadJSON = "/var/www/static"

def nutzerRegistrieren(request):
	matrikelnummer = request.POST.get("matrikelnummer")
	vorname = request.POST.get("vorname")
	nachname = request.POST.get("nachname")
	jahrgang = request.POST.get("jahrgang")
	passwort = request.POST.get("passwort")
	berechtigung = "nutzer"

	nutzerDaten = {
		"matrikelnummer": matrikelnummer,
		"vorname": vorname,
		"nachname": nachname,
		"jahrgang": jahrgang,
		"passwort": passwort,
		"berechtigung": berechtigung
	}

	jsonDatei = os.path.join(speicherpfadJSON, "nutzerdatenbank.json")

	with open(jsonDatei, "r") as datei:
		daten = json.load(datei)

		if matrikelnummer in daten["Benutzer"]:
			return redirect("login")
		
		else:
			daten["Benutzer"][matrikelnummer] = nutzerDaten

	with open(jsonDatei, "w") as datei:
		json.dump(daten, datei)
	
	return redirect("login")
