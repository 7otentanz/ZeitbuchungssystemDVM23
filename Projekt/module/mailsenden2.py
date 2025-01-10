import smtplib
from email.message import EmailMessage

def emailsenden():

    adresse = "timhausertim@gmail.com"        # eigene emailadresse
    passwort = "jevtweduoirhiiqh"                   # eigenes Passwort
    emails = "t_hauser@web.de"

    s = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    s.login(adresse, passwort)

    msg = EmailMessage()
    msg["From"] = adresse
    msg["To"] = emails
    msg["Subject"] = "BEtreffzeile in der Email"
    msg.set_content("Hier könnte ihr Inhalt stehe. Super sache.")

    s.send_message(msg)
    print("Mail versendet.")
    s.quit()

emailsenden()