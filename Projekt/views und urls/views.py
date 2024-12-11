from django.shortcuts import render

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
