# Importation des modules
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sqlite3
from fct_database.requete_sql import get_student_data
from time import time, asctime

# pas besoin de spécifier à chaque fois la pièce jointe


# destinataire = email en string , piece_jointe= "nom du fichier.extension", chemin="chemin"
def send_email(expediteur, password, destinataire, msg, subject, piece_jointe=None, chemin=None):
    Fromadd = expediteur  # expediteur
    Toadd = destinataire  # Spécification des destinataires format string

    message = MIMEMultipart()  # Création de l'objet "message"
    message['From'] = Fromadd  # Spécification de l'expéditeur
    message['To'] = Toadd  # Attache du destinataire à l'objet "message"

    message['Subject'] = subject

    # Attache du message à l'objet "message", et encodage en UTF-8
    message.attach(MIMEText(msg.encode('utf-8'), 'plain', 'utf-8'))

    if piece_jointe != None:
        nom_fichier = piece_jointe  # Spécification du nom de la pièce jointe
        piece = open(chemin, "rb")  # Ouverture du fichier
        # Encodage de la pièce jointe en Base64
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((piece).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "piece; filename= %s" % nom_fichier)
        message.attach(part)  # Attache de la pièce jointe à l'objet "message"

    # Connexion au serveur sortant (en précisant son nom et son port)
    serveur = smtplib.SMTP('smtp.gmail.com', 587)
    serveur.starttls()  # Spécification de la sécurisation
    serveur.login(Fromadd, password)  # Authentification
    # Conversion de l'objet "message" en chaine de caractère et encodage en UTF-8
    texte = message.as_string().encode('utf-8')
    Toadds = [Toadd]  # Rassemblement des destinataires
    serveur.sendmail(Fromadd, Toadds, texte)  # Envoi du mail
    serveur.quit()  # Déconnexion du serveur


def send_to_parent_for_absence(liste_absents):
    date = conversion(asctime())

    for id in liste_absents:
        nom, prenom, parent_mail = get_student_data(id)
        msg = "Votre enfant " + nom + " " + prenom + " a été absent le " + date
        subject = "absence de " + nom + " " + \
            prenom  # Spécification de l'objet de votre mail

        send_email("face.recognation45@gmail.com", "QU42zjpJ4",
                   parent_mail, msg, subject)


def send_to_parent_for_delay(liste_retardataires):
    date = conversion(asctime())

    for coupleIdDuree in liste_retardataires:
        nom, prenom, parent_mail = get_student_data(coupleIdDuree[0])
        msg = "Votre enfant " + nom + " " + prenom + \
            " a été en retard le " + date + " de " + coupleIdDuree[1]
        subject = "Retard de " + nom + " " + prenom

        send_email("face.recognation45@gmail.com",
                   "QU42zjpJ4", parent_mail, msg, subject)


def send_to_manager(manager, piece_jointe, chemin):
    msg = "Voici la liste des absents et des retardataires"
    subject = "Liste des retardataires et des absents"
    send_email("face.recognation45@gmail.com", "QU42zjpJ4",
               manager, msg, subject, piece_jointe, chemin)


def conversion(date):  # prend en argument une date au format asctime() et renvoie une date au format fr
    day = date[0:3]
    month = date[4:7]
    num = date[8:10]
    conv_jours = {"Mon": "Lundi", "Tue": "Mardi", "Wed": "Mercredi",
                  "Thu": "Jeudi", "Fri": "Vendredi", "Sat": "Samedi", "Sun": "Dimanche"}
    conv_mois = {"Jan": "Janvier", "Feb": "Fevrier", "Mar": "Mars", "Apr": "Avril", "May": "Mai", "Jun": "Juin",
                 "Jul": "Juillet", "Aug": "Aout", "Sep": "Septembre", "Oct": "Octobre", "Nov": "Novembre", "Dec": "Decembre"}
    return conv_jours[day]+" "+num+" "+conv_mois[month]
