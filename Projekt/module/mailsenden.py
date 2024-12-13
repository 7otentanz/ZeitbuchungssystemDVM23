import smtplib
from email.message import EmailMessage

adresse = "tenpm@web.de"        # eigene emailadresse
passwort = ""       # eigenes Passwort

def emailsenden():

    s = smtplib.SMTP(host="smtp.web.de", port=587)
    s.starttls()
    s.login(adresse, passwort)

    msg = EmailMessage()
    msg["From"] = adresse
    msg["To"] = "t_hauser@web.de"
    msg["Subject"] = "Testmail!"
    msg.set_content("Ja moin, jetzt ist hier auch\nInhalt")

    s.send_message(msg)

    s.quit()

emailsenden()
