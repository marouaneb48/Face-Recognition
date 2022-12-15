from fct_image_video.detection_redimensionnement import DetecRedim
import os
from matplotlib import pyplot
import numpy as np
from fct_fichiertxt.txt_process import createDirectories, getList
from fct_database.database_building_and_update import getVector
from utils import distanceEuclidienne
from fct_database.requete_sql import get_student_id

import keras.models
model = keras.models.load_model("Modèle VGG")

# Renvoie une matrice de prédiction selon modele des images (à remplacer par genereInputOutput je pense)
def generePrediction(dossierDeDossiersDImages, modele):
    listeToutesLesPhotos = []
    listeNomsDossiers = os.listdir(dossierDeDossiersDImages)
    for nomDossier in listeNomsDossiers:
        if nomDossier != '.DS_Store':
            listeNomsPhotos = os.listdir(
                dossierDeDossiersDImages+'/'+nomDossier)
            for nomPhoto in listeNomsPhotos:
                photo = pyplot.imread(
                    dossierDeDossiersDImages+'/'+nomDossier+'/'+nomPhoto)
                image = cv2.resize(photo, (224, 224))
                listeToutesLesPhotos.append(image)
    listeToutesLesPhotos = np.array(listeToutesLesPhotos)
    return modele.predict(listeToutesLesPhotos)


# Pour une image de visage donnée, renvoie le nom/prénom de la personne inscrite dans la BDD la plus similaire au
# sens du vecteur de représentation selon model.
def nearestNeightbor(imageVisage, model, database='./database/'):
    vectSearchedFace = model.predict(np.array([imageVisage]))[0]
    if type(imageVisage) == str:
        return None

    # On parcours la DB en actualisant si on trouve une ressemblance plus intense que ce qu'on avait déjà
    else:

        dist_min = float('inf')
        completeNameNearestNeightbor = None
        photoNearestNeightbor = None
        for nomEtudiant in os.listdir(database+"students_vectors"):
            for nomFichier in os.listdir(database+"students_vectors/"+nomEtudiant):
                vectNeightbor = getVector(
                    database+"students_vectors/"+nomEtudiant+'/'+nomFichier)
                dist = distanceEuclidienne(vectSearchedFace, vectNeightbor)
                if dist_min > dist:
                    dist_min = dist
                    completeNameNearestNeightbor = nomEtudiant
                    photoNearestNeightbor = database+"students_photos/"+nomEtudiant+'/'+nomFichier
        if completeNameNearestNeightbor == None:
            print(
                "Erreur : aucun étudiant ne possède de photos de lui dans la base de donnée.")
        else:
            listeNomPrenom = completeNameNearestNeightbor.split('_')
            IdVoisin = get_student_id(listeNomPrenom[1], listeNomPrenom[0])
            return IdVoisin, completeNameNearestNeightbor, photoNearestNeightbor, dist_min

#Renvoie si la DB possède assez de photos de visages pour un kNN
def hasEnoughPhotos(cur, k, database):
    for name_lastname in os.listdir(database+"students_photos"):
        name, lastname = name_lastname.split('_')
        Id = get_student_id(lastname, name)
        number_faces_student = cur.execute("SELECT COUNT(*) FROM Faces WHERE student_id = (?)",(Id,)).fetchall()[0][0]
        if k>number_faces_student:
            return False
    return True

#Renvoie la classe ("name_lastname") des visages les plus proches selon kNN et model de imageVisage 
def kNearestNeightbors(imageVisage, model, k, database="./"):
    score = {}
    listeClasses = getList("personnes.txt")
    for classe in listeClasses:
        score[classe] = 0
    listVectAlreadyNear = []
    vectSearchedFace = model.predict(np.array([imageVisage]))[0]

    if os.listdir(database+"students_vectors") == []:
        print("Erreur : Base de donnée vide.")

    # On s'assure que tous les étudiants possèdent au moins k photos
    if not hasEnoughPhotos(k, database):
        print("Alerte : certains étudiants possèdent moins de {} photos, utilisation de NN plutot que kNN".format(k))
        return nearestNeightbor(imageVisage, model, database)
        
    # k fois,
    for i in range(k):
        dist_min = float('inf')
        completeNameOneOfNearestNeightbor = None
        vectOneOfNearestNeightbor = None

        # On parcours la DB
        for nomEtudiant in os.listdir(database+"students_vectors"):
            for nomFichier in os.listdir(database+"students_vectors/"+nomEtudiant):
                # Pour chaque photo de la DB donc chaque vecteur,
                vectFile = database+"students_vectors/"+nomEtudiant+'/'+nomFichier
                # print(vectFile)
                # print(listVectAlreadyNear)
                # print(score)
                # On s'assure que ce n'est pas déjà l'une des k photos proche
                if not vectFile in listVectAlreadyNear:
                    vectNeightbor = getVector(vectFile)
                    dist = distanceEuclidienne(vectSearchedFace, vectNeightbor)

                    # Si la photo est plus proche que les précédentes,

                    if dist_min > dist:
                        dist_min = dist
                        completeNameOneOfNearestNeightbor = nomEtudiant
                        vectOneOfNearestNeightbor = vectFile

        # On a trouvé le plus proche, on ajoute la photo à celles proches et on augmente de 1 le score du voisin proche
        score[completeNameOneOfNearestNeightbor] += 1
        listVectAlreadyNear.append(vectOneOfNearestNeightbor)

    nbrOccurencesMaximale = max(list(score.values()))
    for completeName, nbr in score.items():
        if nbr == nbrOccurencesMaximale:
            neightborCompleteName = completeName
    name, lastname = neightborCompleteName.split('_')
    return {'neightbor' : neightborCompleteName , 'id' : get_student_id(lastname, name)}
    
def getListeId(ListeVisages):
    listeId = []
    for Visage in ListeVisages:
        IdVoisin = nearestNeightbor(Visage, model)[0]
        listeId.append(IdVoisin)
    return listeId


def containsDuplicatas(list):
    for i in range(len(list)):
        for j in range(i+1, len(list)):
            if list[i] == list[j]:
                return True
    return False