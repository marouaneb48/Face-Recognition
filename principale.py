
from fct_image_video.traitement_video import *
from envoi_email import *
from tkinter import *

eleves_attendus = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


def principale(duree):
    liste_visages_temps = ReconnaissanceVisagesVideoListeDeListe(
        lectureVideo(duree))
    liste_absents = absence(liste_visages_temps[0], eleves_attendus)
    liste_retardataires = Retard(
        liste_visages_temps[0], liste_visages_temps[1])
    send_to_parent_for_absence(liste_absents)
    send_to_parent_for_delay(liste_retardataires)
    send_to_manager("maxwolf34@gmail.com", "absentsRetardataires.txt",
                    "./absentsRetardataires.txt")


def action():  # on code l'action du bouton "Valider"
    labelinfo.place_forget()
    duree = int(entrernombre.get())
    principale(duree)
    fichier = open("absentsRetardataires.txt", "r")
    content = fichier.read()
    fichier.close()
    labeltxt = Label(fenetre, text=content)
    labeltxt.place(x=10, y=110)


fenetre = Tk()
fenetre.title("Absences et retards")    # titre de la fenêtre
fenetre.geometry("900x500")             # taille de la fenêtre
#fenetre.attributes("-fullscreen", 1)
b = Button(fenetre, text="Quit", command=fenetre.destroy)   # Bouton "quitter"
b.place(x=825, y=20)
labelnombre = Label(fenetre, text="Entrer la durée de la vidéo : ")
labelnombre.place(x=10, y=20)
entrernombre = Entry(fenetre)
entrernombre.place(x=180, y=20)
labelresultat = Label(
    fenetre, text="Cliquer sur valider pour lancer la vidéo : ")
labelresultat.place(x=10, y=50)
valider = Button(fenetre, text="Valider",          # Bouton "valider"
                 command=action)
valider.place(x=90, y=80)
labelinfo = Label(
    fenetre, text="Le fichier s'ouvrira quand la capture de la vidéo sera terminée")
labelinfo.place(x=5, y=105)

fenetre.mainloop()
