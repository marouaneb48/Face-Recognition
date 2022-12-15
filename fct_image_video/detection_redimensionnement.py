import cv2
from PIL import Image
import os
from matplotlib import pyplot

# A partir d'un fichier image, renvoie une liste d'array représentant les visages trouvés sur l'image, de
# taille 224x224x3


def DetecRedim(CheminAccesImage):
    # Il faut utiliser pyplot pour lire l'image
    
    img = pyplot.imread(CheminAccesImage)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    faces_detecredim = []
    for (x, y, w, h) in faces:
        visage = img[y:y+h, x:x+w]
        visage_redim = cv2.resize(visage, (224, 224))
        faces_detecredim.append(visage_redim)
    return faces_detecredim

# Pareil, mais renvoie le 1er visage sous forme d'array.


def DetecRedimOneFace(CheminAccesImage):
    faces_detecredim = DetecRedim(CheminAccesImage)
    # Si on a trouvé au moins 1 visage, on renvoie le 1er (en espérant que ce soit le bon)
    if faces_detecredim != []:
        return faces_detecredim[0]
    else:
        print("Erreur : aucun visage n'a été détecté sur la photo "+CheminAccesImage)
        return "no_face"


# Crée un visage
def DetecRedimOneFaceAndCreateFaceImage(CheminAccesImage, ext):
    faces_detecredim = DetecRedim(CheminAccesImage)
    # Si on a trouvé au moins 1 visage, on renvoie le 1er (en espérant que ce soit le bon)
    if faces_detecredim != []:
        imageVisage = faces_detecredim[0]
        pilImage = Image.fromarray(imageVisage)
        pilImage.save(CheminAccesImage[-4:]+'FACE.'+ext)
        return CheminAccesImage[-4:]+'FACE.'+ext
    else:
        print("Aucun visage détecté.")

# Crée une photo visage au nom de FACEnomPhoto.ext dans le répertoire folder à partir de la photo filename
# Supprime l'ancienne photo par défaut
# Renvoie le nom du nouveau fichier


def createOneFaceImage(filename, nomPhoto, folder=".", removeFormerPhoto=True):

    imageVisage = DetecRedimOneFace(filename)
    try:
        ext = filename.split('.')[-1]
        chemin = folder+'/FACE'+nomPhoto+'.'+ext
        pilImage = Image.fromarray(imageVisage)
        pilImage.save(chemin)
        if removeFormerPhoto:
            os.remove(filename)
        return chemin
    except:
        pass

# Convertit les images de la DB en image de visage 224x224x3


def createFaceImages(dataset):
    print("Création des visages...")
    from PIL import Image
    for nomDossier in os.listdir(dataset):
        for nomPhoto in os.listdir(dataset+'/'+nomDossier):
            chemin = dataset+'/'+nomDossier+'/'+nomPhoto
            createOneFaceImage(chemin, nomPhoto, dataset+'/'+nomDossier)
