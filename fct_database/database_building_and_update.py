import os
import sqlite3
from matplotlib import pyplot as plt
import cv2
import numpy as np
from fct_fichiertxt.txt_process import createDirectories, getList
from PIL import Image
from utils import norming, distanceEuclidienne
from fct_image_video.detection_redimensionnement import DetecRedim, createOneFaceImage, DetecRedimOneFace
from fct_database.requete_sql import get_student_id
from fct_fichiertxt.txt_process import *

database = "./database/"
conn = sqlite3.connect("RVclasse.db")
cur = conn.cursor()


def resizing224(image):
    return cv2.resize(image, (224, 224))


def extension(photo):
    return photo.split('.')[-1]

# Fonction pour check la DB, à modifier si on le souhaite
def seeDB():
    query1 = "SELECT * FROM Student"
    query2 = "SELECT * FROM Faces"
    print(cur.execute(query1).fetchall())
    print(cur.execute(query2).fetchall())


# Reset la DB en fichier vide (pour pouvoir la recrée après pour tester)
def resetDB():
    open('RVclasse.db', 'w').close()


# Renvoie le vecteur contenu dans un fichier
def getVector(filename):
    file = open(filename, 'r')
    listComp = [float(ligne) for ligne in file]
    return np.array([listComp])[0]


# Ajoute l'étudiant name lastname avec son mail et sa photo principale dans students_photos/lastname_name/. Ajoute
# son vecteur de représentation dans students_vectors/name_lastname
def addStudent(name, lastname, student_mail, parent_mail, photo, removeFormerPhoto=False):
    print("Ajout de l'étudiant {} {} :".format(name, lastname))
    query = "SELECT nom,prenom FROM Student"
    # On vérifie qu'on add pas une personne en double
    if not (lastname, name) in cur.execute(query).fetchall():
        # On vérifie qu'un visage est détecté
        imagesVisages = DetecRedim(photo)
        if imagesVisages == []:
            print("Aucun visage n'est détécté sur la photographie.")
        else:
            # On crée le répertoire /student_photos/Name_Lastname s'il n'existe pas
            import os
            if not os.path.exists(database+"students_photos/"+name+"_"+lastname):
                os.makedirs(database+"students_photos/"+name+"_"+lastname)
                print("Répertoire photo de {} {} créé".format(name, lastname))
            if not os.path.exists(database+"students_vectors/"+name+"_"+lastname):
                os.makedirs(database+"students_vectors/"+name+"_"+lastname)
                print("Répertoire d'identité de {} {} créé".format(name, lastname))

            # On traite photo en en extrayant un visage et en la créant dans students_photos/name_lastname/ au nom
            # de FACENameLastnameMain.ext. On crée l'étudiant dans la DB.
            print("Enregistrement dans la DB de {} {}".format(name, lastname))
            photoVisage = createOneFaceImage(
                photo, name+lastname+"Main", database+"students_photos/"+name+'_'+lastname, removeFormerPhoto)
            query = "INSERT INTO Student(nom, prenom, student_mail, parent_mail, photo_visage, number_faces) VALUES (?,?,?,?,?,?)"
            queryValues = (lastname, name, student_mail,
                           parent_mail, photoVisage, 1)
            cur.execute(query, queryValues)
            conn.commit()

            # On ajoute le visage à la database
            Id = get_student_id(lastname, name)
            query = "INSERT INTO Faces(photo,student_id) VALUES (?,?)"
            queryValues = (photoVisage, Id)
            cur.execute(query, queryValues)
            conn.commit()

            # On calcule le vecteur de représentation par vggCut du visage. On le place dans un fichier
            # /students_vectors/NameLastname/VECTNameLastnameMain
            print("Calcul du vecteur de représentation...")
            from fct_model.models import vggCut
            import keras
            myModel = vggCut()
            vector = myModel.predict(np.array([imagesVisages[0]]))[0]
            print("Création du fichier-vecteur...")
            fichier = open(database+"students_vectors/"+name+'_'+lastname +
                           '/'+"VECT"+name+'_'+lastname+"Main", 'w')
            for comp in vector:
                fichier.write(str(comp)+'\n')
            fichier.close()

            print("Etudiant {} {} ajouté.\n".format(name, lastname))

    else:
        print("L'étudiant {} {} est déjà dans la base de donnée.\n".format(
            name, lastname))



# A partir d'une photo censé être chemin vers un fichier image contenant name lastname, on crée la photo visage du
# 1er visage identifié, son vecteur de représentation, et on ajoute ces chemins dans la DB.
def addFaceAndVector(name, lastname, photo, removeFormerPhoto=True):
    print("Ajout d'une image pour {} {}:".format(name, lastname))
    # On récupère l'id et le nombre number_faces de visage que l'étudiant a déja enregistré
    if get_student_id(lastname, name) == None:
        print("Erreur: {} {} n'est pas dans la base de donnée.\n".format(name, lastname))
    else:
        Id = get_student_id(lastname, name)
        query = "SELECT number_faces FROM Student WHERE id = (?)"
        queryValues = (Id,)
        number_faces = cur.execute(query, queryValues).fetchall()[0][0]
        visage = DetecRedimOneFace(photo)

        # On récupère le vecteur de représentation par le modèle de la photo
        print("Calcul du vecteur de représentation...")
        from fct_model.models import vggCut
        import keras
        myModel = vggCut()
        vector = myModel.predict(np.array([visage]))[0]

        # On ajoute le fichier-vecteur dans students_vectors/Name_Lastname au nom de VECTNameLstnameN+1
        print("Création du fichier-vecteur...")  #a delete peut etre
        fichier = open(database+"students_vectors/"+name+'_'+lastname+'/' +
                    "VECT"+name+'_'+lastname+str(number_faces+1), 'w')
        for comp in vector:
            fichier.write(str(comp)+'\n')
        fichier.close()

        # On ajoute la photo dans students_photos/Name_Lastname au nom de FACEName_LastnameN+1.ext
        print("Ajout de la photo dans le dossier...")
        createOneFaceImage(photo, name+lastname+str(
            number_faces+1), database+"students_photos/"+name+'_'+lastname, removeFormerPhoto)

    

        # On ajoute la photo à la table Faces
        print("Ajout de la photo dans la DB...")
        ext = photo.split('.')[-1]
        query = "INSERT INTO Faces(photo, student_id) VALUES (?,?)"
        queryValues = (database+"students_photos/"+name+'_'+lastname+'/' +
                    "FACE"+name+'_'+lastname+str(number_faces+1)+'.'+ext, Id)
        cur.execute(query, queryValues)

        # On rajoute 1 à number_faces de l'étudiant
        print("Mise à jour de la DB...")
        query = "UPDATE Student SET number_faces = (?)"
        queryValues = (number_faces+1,)
        cur.execute(query, queryValues)
        conn.commit()

        print("La photo a bien été enregistrée.\n")



def buildDatabase3(fichierClasses, database, removeFormerPhoto=False):
    #On crée les dossiers qui gère les visages et leur vecteur de représentation par le modèle VGG
    listeClasses = createDirectories(database+"students_photos", "personnes.txt")
    createDirectories(database+"students_vectors", "personnes.txt")

    for classe in listeClasses:
        name, lastname = classe.split('_')
        pathToPhotos = database+"photos/"+classe+'/'
        weCanAdd = False

        #On vérifie qu'il y a au moins une photo chez l'étudiant
        try:
            photo1 = os.listdir(pathToPhotos)[0]
            print("Photo principale trouvée pour "+lastname)
            weCanAdd = True
        except:
            print("Etudiant {} {} n'a pas de photos".format(name, lastname))

        #On ajoute l'étudiant à la DB avec le visage trouvé sur cette photo 
        # try:
        if weCanAdd:
            addStudent(name, lastname, name+lastname+"@mail", "Parent" +
                        lastname+"@mail", pathToPhotos+photo1, removeFormerPhoto)
        # except:
        #     print("Echec enregistrement de l'étudiant "+name+' '+lastname)

        #On rajoute les autres visages extraits des autres photos
        for photo in os.listdir(pathToPhotos)[1:]:
            try:
                addFaceAndVector(name, lastname, pathToPhotos+
                                 photo, removeFormerPhoto)
            except:
                print("Echec enregistrement d'une photo de l'étudiant " +
                      name+' '+lastname)
        print("")