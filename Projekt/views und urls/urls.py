"""
URL configuration for zeiterfassung project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from ten_pm import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('woranarbeitestdu', views.woranarbeitestdu, name='woranArbeitestDu'),
    path('berichtanlegen', views.berichtAnlegen, name='berichtAnlegen'),
    path('erzaehlmirmehr', views.erzaehlmirmehr, name='erzaehlMirMehr'),
    path('berichtTexterzaehl', views.berichtTexterzaehl, name="berichtTexterzaehl"),
    path('berichtTextkuerzlich', views.berichtTextkuerzlich, name="berichtTextkuerzlich"),
    path('kuerzlichabgeschlossen', views.kuerzlichabgeschlossen, name='kuerzlichAbgeschlossen'),
    path('lassmichdaszusammenfassen', views.lassmichdaszusammenfassen, name='lassMichDasZusammenfassen'),
    path('jsondownload', views.jsondownload, name='jsondownload'),
    path('csvdownload', views.csvdownload, name='csvdownload'),
    path('xmldownload', views.xmldownload, name='xmldownload'),
    path('pdfdownload', views.pdfdownload, name='pdfdownload'),
    path('nutzerverwaltung', views.nutzerverwaltung, name='nutzerverwaltung'),
    path('login', views.login, name='login'),
    path('nutzeranmelden', views.nutzerAnmelden, name='nutzerAnmelden'),
    path('nutzerabmelden', views.nutzerAbmelden, name='nutzerAbmelden'),
    path('registrieren', views.registrieren, name='registrieren'),
    path('nutzerRegistrieren', views.nutzerRegistrieren, name='nutzerRegistrieren'),
    path('berechtigungsantrag', views.berechtigungsantrag, name='berechtigungsantrag'),
    path('antragablehnen', views.antragAblehnen, name='antragAblehnen'),
    path('antraggenehmigen', views.antragGenehmigen, name='antragGenehmigen'),
    path('nutzersperren', views.nutzersperren, name='nutzersperren'),
]

urlpatterns += staticfiles_urlpatterns()
