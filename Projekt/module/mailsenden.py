import smtplib
from email.message import EmailMessage

def emailsenden():
    adresse = "tenpm@web.de"        # eigene emailadresse
    passwort = ""                   # eigenes Passwort
    emails = ["t_hauser@web.de"]

    for mail in emails:
        s = smtplib.SMTP("smtp.web.de", 587)
        s.starttls()
        s.login(adresse, passwort)
        msg = EmailMessage()
        msg["From"] = adresse
        msg["To"] = mail
        msg["Subject"] = betreff
        msg.set_content(inhalt)
        s.send_message(msg)
        s.quit()