from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plot		# Achtung, matplotlib muss IN DER VIRTUAL ENVIRONMENT installiert werden! ### pip install matplotlib ###
import numpy as np
import json
import csv
from lxml import etree	# Achtung, lxml muss IN DER VIRTUAL ENVIRONMENT installiert werden! ### sudo pip install lxml ###
from fpdf import FPDF	# Achtung, fpdf muss IN DER VIRTUAL ENVIRONMENT installiert werden! ### sudo pip install fpdf ###
import smtplib
from email.message import EmailMessage
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

def diagrammberichte(request):
	matrikelnummer = request.session["matrikelnummer"]
	jsonDatei = os.path.join(speicherpfadJSON, "Nutzerberichte", f"berichte_{matrikelnummer}.json")

	gesamtarbeitszeit = []
	technischeDimension = []
	verwaltungsmanagement = []
	rechtlicheGrundlagen = []
	digitalLeadership = []
	bachelorarbeit = []

	with open(jsonDatei, "r", encoding="utf-8") as datei:
		daten = json.load(datei)
		alleBerichte = daten.get("Berichte", [])
	
	for bericht in alleBerichte:
		gesamtarbeitszeit.append(bericht["arbeitszeit"])
		modul = bericht["teilmodul"].split(".")
		if modul[0] == "1":
			technischeDimension.append(int(bericht["arbeitszeit"]))
		elif modul[0] == "2":
			verwaltungsmanagement.append(int(bericht["arbeitszeit"]))
		elif modul[0] == "3":
			rechtlicheGrundlagen.append(int(bericht["arbeitszeit"]))
		elif modul[0] == "4":
			digitalLeadership.append(int(bericht["arbeitszeit"]))
		elif modul[0] == "7":
			bachelorarbeit.append(int(bericht["arbeitszeit"]))
		else:
			pass

	technischeDimensionSumme = sum(technischeDimension)
	verwaltungsmanagementSumme = sum(verwaltungsmanagement)
	rechtlicheGrundlagenSumme = sum(rechtlicheGrundlagen)
	digitalLeadershipSumme = sum(digitalLeadership)
	bachelorarbeitSumme = sum(bachelorarbeit)

	modulgruppen = "Technische Dimension\nder Digitalisierung", "Verwaltungsmanagement", "Rechtliche Grundlagen\nder öff. Verwaltung", "Digital Leadership", "Bachelorarbeit"
	zeiten = [technischeDimensionSumme, verwaltungsmanagementSumme, rechtlicheGrundlagenSumme, digitalLeadershipSumme, bachelorarbeitSumme]
	gesamtarbeitszeit = sum(zeiten)

	fig, ax = plot.subplots()
	ax.pie(zeiten, labels=modulgruppen, autopct= lambda p:f"{p: .1f}%\n{p*gesamtarbeitszeit/100: .0f} Minuten")
	diagrammPNG = os.path.join(speicherpfadJSON, "Nutzerberichte", f"diagramm_{matrikelnummer}.png")
	with open(diagrammPNG, "w") as leereDatei:
		leereDatei.write("Kein Inhalt.")
	plot.savefig(diagrammPNG, format="png", facecolor="#c6debc")
	plot.close(fig)

	parameter = {"Gesamtarbeitszeit": gesamtarbeitszeit}
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
	try:
		parameter = loginPruefen(request)
		parameter.update(nutzerberichte(request))
		return render(request, 'erzaehlMirMehr.html', parameter)
	except:
		return render (request,'erzaehlMirMehr.html')

def kuerzlichabgeschlossen(request):
	try:
		parameter = loginPruefen(request)
		alleBerichte = nutzerberichte(request).get("alleBerichte", [])
		jetzt = datetime.now()
		kürzlich = jetzt - timedelta(hours=3)

		berichteKuerzlich = []
		for bericht in alleBerichte:
			try:
				if "endzeit" in bericht and bericht["endzeit"]:
					endzeit = datetime.strptime(bericht["endzeit"], "%H:%M %d.%m.%y")
					if endzeit > kürzlich:
						berichteKuerzlich.append(bericht)
			except:
				pass

		parameter.update({"alleBerichte": berichteKuerzlich})

		return render(request, 'kuerzlichAbgeschlossen.html', parameter)
	except:
		return render (request,'kuerzlichAbgeschlossen.html')

def lassmichdaszusammenfassen(request):
	diagrammberichte(request)
	try:
		parameter = loginPruefen(request)
		parameter.update(nutzerberichte(request))
		parameter.update(diagrammberichte(request))
		return render(request, 'lassMichDasZusammenfassen.html', parameter)
	except:
		return render (request,'lassMichDasZusammenfassen.html')

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
				request.session["matrikelnummer"] = matrikelnummer
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

### Bericht anlegen und mit einer Startzeit versehen ###

def berichtAnlegen(request):

	if request.method == "POST":
		
		matrikelnummer = request.session["matrikelnummer"]
		id = request.POST.get('id')
		teilmodul = request.POST.get("teilmodul")
		jsonDatei = os.path.join(speicherpfadJSON, "Nutzerberichte", f"berichte_{matrikelnummer}.json")
		
		if not id:
			startzeit = datetime.now()
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
			
			parameter = loginPruefen(request)
			parameter.update({"id": str(neuerBericht.id), "teilmodul": str(neuerBericht.teilmodul)})

			return render(request, 'woranArbeitestDu.html', parameter)
		
		else:
			endzeit = datetime.now()

			with open(jsonDatei, "r", encoding="utf-8") as datei:
				daten = json.load(datei)
				bestehendeBerichte = daten.get("Berichte", [])

			for bericht in bestehendeBerichte:
				if str(bericht["id"]) == id:
					bericht["endzeit"] = endzeit.strftime("%R %d.%m.%y")
					teilmodul = bericht["teilmodul"]
					
			with open(jsonDatei, "w", encoding="utf-8") as datei:
				json.dump({"Berichte": bestehendeBerichte}, datei, indent=4)

			parameter = loginPruefen(request)
			parameter.update({"id": None, "teilmodul" : teilmodul}) #Id solle eigentlich "gelöscht" werden, hier also >id: None<?
			return render(request, 'woranArbeitestDu.html', parameter)

### Bericht mit einem Text versehen ###

def berichtText(request):

	if request.method == "POST":

		id = request.POST.get("id")
		text = request.POST.get("text")
		matrikelnummer = request.session.get("matrikelnummer")
	jsonDatei = os.path.join(speicherpfadJSON, "Nutzerberichte", f"berichte_{matrikelnummer}.json")

	with open(jsonDatei, "r", encoding="utf-8") as datei:
		daten = json.load(datei)
		berichte = daten.get("Berichte",[])

	for bericht in berichte:
		if bericht["id"] == id:
			bericht["text"] = text
		
	with open(jsonDatei, "w", encoding="utf-8") as datei:
		json.dump({"Berichte": berichte}, datei, indent=4)

def berichtTexterzaehl(request):
	berichtText(request)
	return redirect("erzaehlMirMehr")

def berichtTextkuerzlich(request):
	berichtText(request)
	return redirect("kuerzlichAbgeschlossen")

### Alle Nutzerberichte als json herunterladen ###

def jsondownload(request):

	if request.method =="POST":

		parameter = nutzerberichte(request)
		alleBerichte = parameter.get("alleBerichte", [])
		downloadberichte = []

		for bericht in alleBerichte:
			if bericht["endzeit"] != 0 and bericht["text"] != "":
				downloadberichte.append(bericht)
		
		jsonberichte = {"Berichte": downloadberichte}
		jsondatei = json.dumps(jsonberichte, indent=4)

		response = HttpResponse(jsondatei, content_type="application/json")
		response["Content-Disposition"] = 'attachment; filename="berichte.json"'
		return response

### Alle Nutzerberichte als csv herunterladen ###

def csvdownload(request):

	if request.method =="POST":

		parameter = nutzerberichte(request)
		alleBerichte = parameter.get("alleBerichte", [])
		downloadberichte = []

		for bericht in alleBerichte:
			if bericht["endzeit"] != 0 and bericht["text"] != "":
				downloadberichte.append(bericht)

		response = HttpResponse(content_type="text/csv")
		response["Content-Disposition"] = 'attachment; filename="berichte.csv"'

		csvtabelle = csv.DictWriter(response, fieldnames=["startzeit", "teilmodul", "endzeit", "text", "arbeitszeit", "id"], delimiter=";")
		csvtabelle.writeheader()

		for bericht in downloadberichte:
			csvtabelle.writerow(bericht)
		return response

### Alle Nutzerberichte als xml herunterladen ###

def xmldownload(request):

	if request.method == "POST":

		parameter = nutzerberichte(request)
		alleBerichte = parameter.get("alleBerichte", [])
		downloadberichte = []

		for bericht in alleBerichte:
			if bericht["endzeit"] != 0 and bericht["text"] != "":
				downloadberichte.append(bericht)
		
		root = etree.Element("Berichte")

		for bericht in downloadberichte:
			einbericht = etree.SubElement(root, "Bericht")
			for key, value in bericht.items():
				etree.SubElement(einbericht, key).text = str(value)
		
		tree = etree.ElementTree(root)
		response = HttpResponse(content_type="application/xml")
		response["Content-Disposition"] = 'attachment; filename="berichte.xml"'
		tree.write(response)
		return response

### Alle Nutzerberichte als pdf herunterladen ###

def pdfdownload(request):

	if request.method == "POST":

		parameter = nutzerberichte(request)
		alleBerichte = parameter.get("alleBerichte", [])
		downloadberichte = []

		for bericht in alleBerichte:
			if bericht["endzeit"] != 0 and bericht["text"] != "":
				downloadberichte.append(bericht)

		matrikelnummer = request.session["matrikelnummer"]

		pdf = FPDF()
		pdf.add_page()
		pdf.set_fill_color(255, 189, 89)
		pdf.rect(0, 0, 210, 33.5, "F")
		pdf.image(os.path.join(speicherpfadJSON, "Logoentwurf.png"), x=5, y=5, w=37.5, h=28.5)

		pdf.set_font("Arial", style="B", size=16)
		pdf.cell(0, 11, f"Berichte von {matrikelnummer}", ln=True, align='C')
		pdf.ln(15)
		pdf.image(os.path.join(speicherpfadJSON, "Nutzerberichte", f"diagramm_{matrikelnummer}.png"), x=40, y=pdf.get_y(), w=130)
		pdf.ln(100)
		pdf.line(10, pdf.get_y(), 200, pdf.get_y())
		
		for bericht in downloadberichte:
			arbeitszeit = str(bericht["arbeitszeit"])
			pdf.set_font("Arial", style="B", size=11)
			pdf.cell(0, 10, f"{arbeitszeit} Minuten von {bericht["startzeit"]} bis {bericht["endzeit"]}", ln=True)
			pdf.cell(0, 10, f"{bericht["teilmodul"]}", ln=True)
			pdf.set_font("Arial", size=11)
			pdf.multi_cell(0, 10, f"Folgendes wurde in dieser Zeit bearbeitet:\n  {bericht["text"]}")
			pdf.ln(5)
			pdf.line(10, pdf.get_y(), 200, pdf.get_y())

		fertigespdf = pdf.output(dest="S").encode("latin1")
		response = HttpResponse(fertigespdf, content_type="application/pdf")
		response["Content-Disposition"] = 'attachment; filename="berichte.pdf"'
		return response

### Berichte hochladen und damit die eigenen Berichte auf dem Server aktualisieren ###

def berichtehochladen(request):

	if request.method == "POST":

		matrikelnummer = request.session["matrikelnummer"]
		hochgeladenedatei = request.FILES["datei"]
		dateiname= hochgeladenedatei.name
		jsonDatei = os.path.join(speicherpfadJSON, "Nutzerberichte", f"berichte_{matrikelnummer}.json")

		if os.path.exists(jsonDatei):
			with open(jsonDatei, "r", encoding="utf-8") as datei:
				daten = json.load(datei)
				alteBerichte = daten.get("Berichte",[])
		else:
			alteBerichte = []

		if dateiname.endswith(".json"):
			neueBerichte = json.load(hochgeladenedatei)

		elif dateiname.endswith(".csv"):
			inhaltcsv = hochgeladenedatei.read().decode("utf-8")
			csvinhalt = csv.DictReader(inhaltcsv.splitlines(), delimiter=";")
			hochgeladeneberichte = []
			for bericht in csvinhalt:
				hochgeladeneberichte.append(bericht)
			neueBerichte = {"Berichte": hochgeladeneberichte}

		elif dateiname.endswith(".xml"):
			tree = etree.parse(hochgeladenedatei)
			neueBerichte = {"Berichte": []}
			for einbericht in tree.xpath(".//Bericht"):
				bericht = {}
				for detail in einbericht:
					bericht[detail.tag] = detail.text
				neueBerichte["Berichte"].append(bericht)
		else:
			return HttpResponse("<script>alert('Verwende .json, .csv oder .xml!');window.history.back()</script>")

		for neuerbericht in neueBerichte["Berichte"]:
			existiert = False
			for alterbericht in alteBerichte:
				if alterbericht["id"] == neuerbericht["id"]:
					alterbericht.update(neuerbericht)
					existiert = True
					break
			if not existiert:
				alteBerichte.append(neuerbericht)

		alleBerichte = {"Berichte": alteBerichte}

		with open(jsonDatei, "w", encoding="utf-8") as datei:
			json.dump(alleBerichte, datei, indent=4)

		return redirect("lassMichDasZusammenfassen")

### Email senden - allgemeine Funktion ###

def emailsenden(emails, betreff, inhalt):

	adresse = "tenpm.app@gmail.com"
	passwort = "gouiipozoxvkecgl "

	server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
	server.login(adresse, passwort)

	for email in emails:
		msg = EmailMessage()
		msg["From"] = adresse
		msg["To"] = email
		msg["Subject"] = betreff
		msg.set_content(inhalt)
		server.send_message(msg)
	
	server.quit()

### Berechtigungsantrag verschicken, für alle, die noch nicht Admin sind ###

def berechtigungsantrag(request):

	if request.method =="POST":

		jsonDatei = os.path.join(speicherpfadJSON, "berechtigungsantraege.json")
		berechtigung = request.session["berechtigung"]
		matrikelnummer = request.session["matrikelnummer"]

		if berechtigung == "nutzer":
			email = None
			antragAls = "vip"
		elif berechtigung == "vip":
			email = request.POST.get("email")
			antragAls = "admin"
		elif berechtigung == "gesperrt":
			email = None
			antragAls = "nutzer"

		with open(jsonDatei, "r", encoding="utf-8") as datei:
			daten = json.load(datei)
			if matrikelnummer in daten["Anträge"]:
				daten["Anträge"][matrikelnummer]["antragAls"] = antragAls
				daten["Anträge"][matrikelnummer]["email"] = email
			else:
				einAntrag = {"antragAls": antragAls, "email": email}
				daten["Anträge"][matrikelnummer] = einAntrag

		with open(jsonDatei, "w", encoding="utf-8") as datei:
			json.dump(daten, datei, indent=4)
		
		jsonDatei = os.path.join(speicherpfadJSON, "nutzerdatenbank.json")
		adminmails = []

		with open(jsonDatei, "r", encoding="utf-8") as datei:
			daten = json.load(datei)
			for benutzer in daten["Benutzer"].values():
				if benutzer.get("email"):
					adminmails.append(benutzer["email"])

		betreff = "Neuer Berechtigungsantrag"
		inhalt = f"""
Hallo liebe Admins,\n\n
der Nutzer mit der Matrikelnummer {matrikelnummer} beantragt den Status {antragAls}.\n
Logge dich auf 10PM ein um den Antrag zu genehmigen oder abzulehnen!\n\n
Danke für deine Unterstützung!
""" 
		
		emailsenden(adminmails, betreff, inhalt)

		return redirect("nutzerverwaltung")

### Anträge, die bearbeitet wurde, müssen auch wieder aus der Übersicht entfernt werden ###

def antragEntfernen(request):

	jsonDatei = os.path.join(speicherpfadJSON, "berechtigungsantraege.json")
	with open(jsonDatei, "r", encoding="utf-8") as datei:	
		daten = json.load(datei)
		print(daten)
		matrikelnummer = request.POST.get("matrikelnummer")
		daten["Anträge"].pop(matrikelnummer)
		
	with open(jsonDatei, "w", encoding="utf-8") as datei:
		json.dump(daten, datei, indent=4)

### Antrag ablehen und alten Status des Nutzers beibehalten ###

def antragAblehnen(request):
	
	if request.method =="POST":
		antragEntfernen(request)
		return redirect("nutzerverwaltung")

### Antrag genehmigen und Nutzer neuen Status zuteilen ###

def antragGenehmigen(request):

	if request.method =="POST":

		matrikelnummer = request.POST.get("matrikelnummer")
		jsonDatei = os.path.join(speicherpfadJSON, "berechtigungsantraege.json")

		with open(jsonDatei, "r", encoding="utf-8") as datei:
			daten = json.load(datei)
			antragAls = daten["Anträge"][matrikelnummer]["antragAls"]
			email = daten["Anträge"][matrikelnummer]["email"]

		jsonDatei = os.path.join(speicherpfadJSON, "nutzerdatenbank.json")

		with open(jsonDatei, "r", encoding="utf-8") as datei:
			daten = json.load(datei)

			daten["Benutzer"][matrikelnummer]["berechtigung"] = antragAls
			daten["Benutzer"][matrikelnummer]["email"] = email
		
		with open(jsonDatei, "w", encoding="utf-8") as datei:
			json.dump(daten, datei, indent=4)
		
		antragEntfernen(request)
		return redirect("nutzerverwaltung")

### Nutzer sperren, sodass nichts mehr verwendet werden kann ###

def nutzersperren(request):

	if request.method == "POST":

		matrikelnummer = request.POST.get("matrikelnummer")
		jsonDatei = os.path.join(speicherpfadJSON, "nutzerdatenbank.json")

		with open(jsonDatei, "r", encoding="utf-8") as datei:
			daten = json.load(datei)
			daten["Benutzer"][matrikelnummer]["berechtigung"] = "gesperrt"
		
		with open(jsonDatei, "w", encoding="utf-8") as datei:
			json.dump(daten, datei, indent=4)
		return redirect("nutzerverwaltung")

### Änderung des Modulhandbuchs an die Webmaster melden ###

def antragmodulhandbuch(request):

	if request.method == "POST":

		matrikelnummer = request.session["matrikelnummer"]
		webmaster = ["hauser_tim@teams.hs-ludwigsburg.de", "pfefferkorn_laura@teams.hs-ludwigsburg.de"]
		betreff = "ACHTUNG! Eine Änderung des Modulhandbuchs steht bevor!"
		inhalt = f"""
Hallo Laura, hallo Tim,\n
der Nutzer mit der Matrikelnummer {matrikelnummer} hat das Formular für Änderungen des Modulhandbuchs verwendet.\n
Das ist der Text, den er übermittelt:\n\n
"{request.POST.get("text")}"\n\n
Bitte fügt diese Änderungen entsprechend auf dem "Woran arbeitest du gerade?"-Template ein.\n
Herzlichste Grüße!
"""
		emailsenden(webmaster, betreff, inhalt)
		return redirect("nutzerverwaltung")
