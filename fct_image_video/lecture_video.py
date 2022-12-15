import cv2
from time import time, asctime
import os
from PIL import Image


def lectureVideo(duree):

    # On ouvre la caméra et on filme ou on choisit une vidéo (la vidéo prise n'est donc pas directement stockée, seules les images le sont)
    # le premier argument permet de choisir la caméra qui va tourner ou mettre le chemin d'une video pour la lire directement
    cap = cv2.VideoCapture('./InShot_20201119_100829799.mp4')
    debut = time()
    i = 0
    liste_photos = []  # liste de couples de la forme (image,date)
    files = os.listdir("./decoupage_video")
    for i in range(len(files)):                   # on vide le dossier decoupage_video
        os.remove("./decoupage_video/"+files[i])
    while(cap.isOpened()):
        _, frame = cap.read()
        cv2.waitKey(15)
        if not type(frame) == type(None):
            t = asctime()  # date à laqelle l'image est capturée (t est une chaîne de caractères)
            i += 1
            # on divise les FPS par 15 (on prend une image sur 15)
            if i % 15 == 0:
                chemin = './decoupage_video/image'+str((i//15)-2)+'.jpg'
                cv2.imwrite(chemin, frame)
                liste_photos.append((chemin, t))
            if time()-debut > duree:
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    return liste_photos
