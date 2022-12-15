from fct_image_video.detection_redimensionnement import DetecRedim
from fct_image_video.lecture_video import lectureVideo
from matplotlib import pyplot
import cv2
from fct_database.requete_sql import get_student_data
from fct_model.analyse_model import getListeId
import os


def difference(li1, li2):  # renvoie la différence symétrique des listes l1 et l2
    return [x for x in li1 if x not in li2]

# on suppose qu'on a deja une fonction "id" qui donne l'id de la personne sur la photo
# et on suppose connu la liste des élèves "élèves" qui doivent être présents


# ecrit les absents dans un fichier txt et renvoie aussi la liste des absents
def absence(liste_visages, eleves):
    # Attention, liste_visages est une liste de liste de visages
    presents = []
    for k in range(len(liste_visages)):
        identite = getListeId(liste_visages[k])
        for id in identite:
            if id not in presents:
                presents.append(id)
            # élèves est une liste d'id
    absents = difference(eleves, presents)
    with open("absentsRetardataires.txt", "w") as file:
        file.write("Voici les élèves absents aujourd'hui :")
        file.write("\n\n")
        for x in absents:
            Nom_eleve = get_student_data(x)
            file.write(Nom_eleve[0] + " " + Nom_eleve[1])
            file.write("\n")
    return difference(eleves, presents)


def ReconnaissanceVisagesVideoListeDeListe(liste_photos):
    ListeVisages = []
    ListeTemps = []
    for couplePhotoTemps in liste_photos:
        # Pour chaque photo dde la liste de photos, on crée la liste des visages détectés sur la photo
        VisagesDetec = DetecRedim(couplePhotoTemps[0])
        # On crée ainsi la liste des listes des visages
        ListeVisages.append(VisagesDetec)
        # Et la liste des moments coincidant avec chaque liste de visage
        ListeTemps.append(couplePhotoTemps[1])
    return (ListeVisages, ListeTemps)


''' cv2.imshow('img', ReconnaissanceVisagesVideoListeDeListe(
    lectureVideo(5))[0][3][2])
cv2.waitKey(0)
cv2.destroyAllWindows()

print(len(ReconnaissanceVisagesVideoListeDeListe(lectureVideo(5))[0][3])) '''


def HMStoS(date):       # on convertit le format heure:minutes:secondes en secondes
    H = int(date[11:13])
    M = int(date[14:16])
    S = int(date[17:19])
    return H*(60**2) + M*60 + S


def StoHMS(S):             # on convertit un nombre de secondes en minutes+secondes
    M = (S % (60**2))//60
    S = (S % (60**2)) % 60
    # Ne prend pas en compte pluriel ou singulier dans le résultat
    return str(M)+" minutes " + str(S)+" secondes"


# écrit un fichier texte avec les retardataires et leur temps de retard et renvoie la liste des retardataire
def Retard(ListeVisages, ListeTemps):
    # Attention ListeVisages est une liste de liste de visages
    ListeRetardataire = []
    date = ListeTemps[0]
    S_0 = HMStoS(date)  # Référence de temps
    # On prend comme référence pour les retards la première image
    ListeIdPresents_reference = getListeId(ListeVisages[0])
    for i in range(1, len(ListeVisages)):
        ListeIdPresents = getListeId(ListeVisages[i])
        # On regarde quels élèves sont dans la nouvelle photo mais pas celle d'avant
        diff = difference(ListeIdPresents, ListeIdPresents_reference)
        S_1 = HMStoS(ListeTemps[i])
        for Id in diff:
            # Pour chacun de ces élèves, on l'ajoute à la liste de référence pour ne pas le recompter à chaque nouvelle photo
            # et si il est arrivé avant les n premières secondes du cours, il n'est pas comptabilisé commme étant en retard
            ListeIdPresents_reference.append(Id)
            if S_1-S_0 >= 11:
                coupleRetard = (Id, StoHMS(S_1-S_0))
                ListeRetardataire.append(coupleRetard)
    with open('absentsRetardataires.txt', 'a') as file:
        file.write("\n\n")
        file.write("Voici les élèves en retard aujourd'hui:")
        file.write("\n\n")
        if ListeRetardataire != []:
            for x in ListeRetardataire:
                # On réalise ici le fichier texte contenant les retardataires et leur retard
                Nom_eleve = get_student_data(x[0])
                file.write(Nom_eleve[0] + " " + Nom_eleve[1] +
                           " est en retard de " + x[1])
                file.write('\n')
    return ListeRetardataire
