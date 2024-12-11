from django.shortcuts import render
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

speicherpfadJSON = "./static/"		# Hier muss der tatsächliche Speicherort rein!

def nutzerRegistrieren(request):

	matrikelnummer = request.POST.get("matrikelnummer")
	vorname = request.POST.get("vorname")
	nachname = request.POST.get("nachname")
	jahrgang = request.POST.get("jahrgang")
	passwort = request.POST.get("passwort")

	nutzerDaten = {
		"matrikelnummer": matrikelnummer,
		"vorname": vorname,
		"nachname": nachname,
		"jahrgang": jahrgang,
		"passwort": passwort
	}

	jsonDatei = os.path.join(speicherpfadJSON, "nutzerdatenbank.json")

	with open(jsonDatei, "w") as nutzerdatenbank:							# PERMISSION DENIED -- noch keine Lösung.
		json.dump(nutzerDaten, nutzerdatenbank)

	return JsonResponse({"status": "success", "message": "Benutzer registriert!"})
