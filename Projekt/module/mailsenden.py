import smtplib
from email.message import EmailMessage

adresse = "tenpm@web.de"        # eigene emailadresse
passwort = "Mindestens9Zeichen!"       # eigenes Passwort
emails = ["t_hauser@web.de"]


def emailsenden():

    for mail in emails:

        s = smtplib.SMTP_SSL("smtp.web.de", 465)
        s.login(adresse, passwort)

        msg = EmailMessage()
        msg["From"] = adresse
        msg["To"] = mail
        msg["Subject"] = "Testmail!"
        msg.set_content("Ja moin, jetzt ist hier auch\nInhalt")

        s.send_message(msg)

        s.quit()

emailsenden()
